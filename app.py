import streamlit as st
from pathlib import Path

from core.sheets_client import GoogleSheetsClient
from core.pilot_manager import PilotManager
from core.drone_manager import DroneManager
from core.matcher import Matcher
from core.urgent_reassign import UrgentReassigner
from core.nlp_client import NLPClient

# ==================== SETUP ====================
BASE_DIR = Path(__file__).resolve().parent
CREDS_PATH = BASE_DIR / "config" / "credentials.json"

st.set_page_config(
    page_title="Skylark Drone Ops Agent",
    page_icon="🚁",
    layout="wide"
)

st.title("🚁 Skylark Drone Operations Coordinator")
st.caption("Safe assignment with availability check + urgent override")

# ==================== INIT ====================
sheets = GoogleSheetsClient(str(CREDS_PATH))
pilot_manager = PilotManager(sheets)
drone_manager = DroneManager(sheets)
matcher = Matcher()
urgent = UrgentReassigner()
nlp = NLPClient()

# ==================== SESSION ====================
if "stage" not in st.session_state:
    st.session_state.stage = "root"

# ==================== HELPERS ====================
def back(stage):
    if st.button("⬅ Back"):
        st.session_state.stage = stage
        st.rerun()

def get_row(sheet, key_col, key_val):
    ws = sheets.client.open(sheet).worksheet(sheet)
    rows = ws.get_all_records()
    for i, r in enumerate(rows, start=2):
        if str(r.get(key_col, "")).strip().lower() == key_val.lower():
            return i, r
    return None, None

def update_row(sheet, row_idx, values):
    sheets.client.open(sheet).worksheet(sheet).update(f"A{row_idx}", [values])

def is_assigned(mission):
    return str(mission.get("status", "")).lower() == "assigned"

def extract_pilot_drone(s):
    pilot = (
        s.get("pilot")
        or s.get("pilot_name")
        or (s.get("pilot", {}).get("name") if isinstance(s.get("pilot"), dict) else None)
    )
    drone = (
        s.get("drone")
        or s.get("drone_id")
        or (s.get("drone", {}).get("drone_id") if isinstance(s.get("drone"), dict) else None)
    )
    return pilot, drone

def commit_assignment(mission_id, mission, pilot, drone):
    # update mission
    midx, _ = get_row("missions", "project_id", mission_id)
    update_row(
        "missions",
        midx,
        [
            mission_id,
            mission["client"],
            mission["location"],
            mission["required_skills"],
            mission["start_date"],
            mission["end_date"],
            mission["priority"],
            "Assigned",
            pilot,
            drone,
        ],
    )

    # update pilot
    pidx, p = get_row("pilot_roster", "name", pilot)
    update_row(
        "pilot_roster",
        pidx,
        [
            p["name"],
            p["skills"],
            p["certifications"],
            p["drone_experience"],
            p["location"],
            mission_id,
            "Unavailable",
            "No",
        ],
    )

    # update drone
    didx, d = get_row("drone_fleet", "drone_id", drone)
    update_row(
        "drone_fleet",
        didx,
        [
            d["drone_id"],
            d["model"],
            d["capabilities"],
            "Unavailable",
            d["location"],
            d["maintenance_due"],
            mission_id,
        ],
    )

# ==================== ASSIGNMENT FLOW ====================
def assignment_flow(urgent_mode=False):
    mission_id = st.text_input(
        "Mission ID",
        key=f"mission_{'urgent' if urgent_mode else 'normal'}"
    )

    if not mission_id:
        return

    midx, mission = get_row("missions", "project_id", mission_id)
    if not mission:
        st.error("❌ Mission not found")
        return

    if is_assigned(mission) and not urgent_mode:
        st.warning(
            f"⚠️ Already assigned to "
            f"{mission.get('current_pilot')} / {mission.get('current_drone')}"
        )
        return

    st.markdown("### ✅ Available Resources")

    pilots = pilot_manager.get_available_pilots()
    drones = drone_manager.get_available_drones()

    st.write("👨‍✈️ Pilots")
    st.dataframe(pilots, use_container_width=True)

    st.write("🚁 Drones")
    st.dataframe(drones, use_container_width=True)

    st.divider()
    st.markdown("### 🎯 Assignment Suggestions")

    suggestions = (
        urgent.suggest_alternatives(pilots, drones, mission)
        if urgent_mode
        else matcher.match(pilots, drones, mission)
    )

    if not suggestions:
        st.warning("No suitable assignments found")
        return

    for i, s in enumerate(suggestions[:3]):
        pilot, drone = extract_pilot_drone(s)

        if not pilot or not drone:
            continue

        with st.expander(f"Option {i+1}"):
            st.write(f"👨‍✈️ Pilot: **{pilot}**")
            st.write(f"🚁 Drone: **{drone}**")

            if urgent_mode:
                st.warning("⚠️ Urgent override enabled")

            if st.button(
                "Force Assign" if urgent_mode else "Assign",
                key=f"{'u' if urgent_mode else 'n'}_{i}"
            ):
                commit_assignment(mission_id, mission, pilot, drone)
                st.success("✅ Assignment completed & synced to Sheets")
                st.rerun()

# ==================== ROOT ====================
if st.session_state.stage == "root":
    st.subheader("Choose Operation")
    c1, c2, c3 = st.columns(3)
    if c1.button("👨‍✈️ Pilots"):
        st.session_state.stage = "pilot"
    if c2.button("🚁 Drones"):
        st.session_state.stage = "drone"
    if c3.button("🎯 Missions"):
        st.session_state.stage = "mission"

# ==================== PILOTS ====================
elif st.session_state.stage == "pilot":
    st.subheader("👨‍✈️ Available Pilots")
    st.dataframe(pilot_manager.get_available_pilots(), use_container_width=True)
    back("root")

# ==================== DRONES ====================
elif st.session_state.stage == "drone":
    st.subheader("🚁 Available Drones")
    st.dataframe(drone_manager.get_available_drones(), use_container_width=True)
    back("root")

# ==================== MISSIONS ====================
elif st.session_state.stage == "mission":
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("## Normal Assignment")
        assignment_flow(False)
    with c2:
        st.markdown("## 🚨 Urgent Reassign")
        assignment_flow(True)
    back("root")

# ==================== AI CHAT ====================
user = st.chat_input("Try: assign mission M101, urgent reassign M101")
if user:
    intent = nlp.parse(user).get("intent")
    with st.chat_message("assistant"):
        if intent == "assign":
            assignment_flow(False)
        elif intent == "reassign":
            assignment_flow(True)
        elif intent == "query_pilots":
            st.dataframe(pilot_manager.get_available_pilots())
        elif intent == "query_drones":
            st.dataframe(drone_manager.get_available_drones())
