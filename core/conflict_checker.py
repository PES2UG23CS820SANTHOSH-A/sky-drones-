from datetime import datetime
from typing import List, Dict
import pandas as pd


class ConflictChecker:
    def __init__(self):
        pass

    def check_pilot_conflicts(
        self,
        pilot_name: str,
        mission_start: str,
        mission_end: str,
        assignments_df: pd.DataFrame
    ) -> List[str]:
        """
        Check if pilot is double-booked for overlapping missions.
        """
        conflicts = []

        start = datetime.fromisoformat(mission_start)
        end = datetime.fromisoformat(mission_end)

        pilot_assignments = assignments_df[
            assignments_df["pilot_name"].str.lower() == pilot_name.lower()
        ]

        for _, row in pilot_assignments.iterrows():
            a_start = datetime.fromisoformat(row["start date"])
            a_end = datetime.fromisoformat(row["end date"])

            if start <= a_end and end >= a_start:
                conflicts.append(
                    f"Pilot {pilot_name} already assigned to mission {row['project id']}"
                )

        return conflicts

    def check_drone_conflicts(
        self,
        drone_id: str,
        mission_start: str,
        mission_end: str,
        assignments_df: pd.DataFrame
    ) -> List[str]:
        """
        Check if drone is double-booked.
        """
        conflicts = []

        start = datetime.fromisoformat(mission_start)
        end = datetime.fromisoformat(mission_end)

        drone_assignments = assignments_df[
            assignments_df["drone_id"].str.lower() == drone_id.lower()
        ]

        for _, row in drone_assignments.iterrows():
            a_start = datetime.fromisoformat(row["start date"])
            a_end = datetime.fromisoformat(row["end date"])

            if start <= a_end and end >= a_start:
                conflicts.append(
                    f"Drone {drone_id} already assigned to mission {row['project id']}"
                )

        return conflicts

    def check_skill_mismatch(
        self,
        pilot_skills: str,
        required_skill: str
    ) -> List[str]:
        """
        Check if pilot lacks required skill.
        """
        if required_skill.lower() not in pilot_skills.lower():
            return [f"Pilot lacks required skill: {required_skill}"]
        return []

    def check_maintenance(
        self,
        drone_status: str
    ) -> List[str]:
        """
        Check if drone is under maintenance.
        """
        if "maintenance" in drone_status.lower():
            return ["Drone is currently under maintenance"]
        return []

    def check_location_mismatch(
        self,
        pilot_location: str,
        drone_location: str,
        mission_location: str
    ) -> List[str]:
        """
        Check pilot/drone location mismatch with mission.
        """
        warnings = []

        if mission_location.lower() not in pilot_location.lower():
            warnings.append("Pilot location does not match mission location")

        if mission_location.lower() not in drone_location.lower():
            warnings.append("Drone location does not match mission location")

        return warnings
