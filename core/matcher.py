from typing import Dict, List
import pandas as pd

class Matcher:
    def match(
        self,
        pilots_df: pd.DataFrame,
        drones_df: pd.DataFrame,
        mission: Dict
    ) -> List[Dict]:
        """
        Match pilots and drones to a mission.
        Returns a ranked list of possible assignments.
        """

        matches = []

        required_skill = mission.get("required_skills")
        mission_location = mission.get("location")

        for _, pilot in pilots_df.iterrows():

            # ---- Pilot skill check ----
            if required_skill:
                if required_skill.lower() not in str(pilot["skills"]).lower():
                    continue

            for _, drone in drones_df.iterrows():
                score = 0

                # ---- Location match ----
                if mission_location:
                    if mission_location.lower() in str(pilot["location"]).lower():
                        score += 1
                    if mission_location.lower() in str(drone["location"]).lower():
                        score += 1

                # ---- Drone capability match ----
                if required_skill:
                    if required_skill.lower() in str(drone["capabilities"]).lower():
                        score += 1

                matches.append({
                    "pilot_name": pilot["name"],
                    "drone_id": drone["drone_id"],
                    "score": score
                })

        # Sort best matches first
        return sorted(matches, key=lambda x: x["score"], reverse=True)
