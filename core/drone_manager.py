import pandas as pd
from core.sheets_client import GoogleSheetsClient

# File name and worksheet (tab) name are the SAME
DRONE_SHEET = "drone_fleet"
DRONE_WORKSHEET = "drone_fleet"

class DroneManager:
    def __init__(self, sheets_client: GoogleSheetsClient):
        self.sheets = sheets_client

    def load_drones(self) -> pd.DataFrame:
        return self.sheets.read_df(DRONE_SHEET, DRONE_WORKSHEET)

    def get_available_drones(self, capability=None, location=None) -> pd.DataFrame:
        df = self.load_drones()

        # Normalize status and filter available drones
        df = df[df["status"].str.lower() == "available"]

        if capability:
            df = df[df["capabilities"].str.contains(capability, case=False, na=False)]

        if location:
            df = df[df["location"].str.contains(location, case=False, na=False)]

        return df

    def get_drones_in_maintenance(self) -> pd.DataFrame:
        df = self.load_drones()
        return df[df["status"].str.contains("maintenance", case=False, na=False)]

    def update_drone_status(self, drone_id: str, new_status: str) -> bool:
        ws = self.sheets.client.open(DRONE_SHEET).worksheet(DRONE_WORKSHEET)
        records = ws.get_all_records()

        for idx, row in enumerate(records, start=2):
            if row["drone_id"].strip().lower() == drone_id.strip().lower():
                status_col = list(row.keys()).index("status") + 1
                ws.update_cell(idx, status_col, new_status)
                return True

        return False
