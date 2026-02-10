import pandas as pd
from core.sheets_client import GoogleSheetsClient

# File name and tab name are the SAME
PILOT_SHEET = "pilot_roster"
PILOT_WORKSHEET = "pilot_roster"

class PilotManager:
    def __init__(self, sheets_client: GoogleSheetsClient):
        self.sheets = sheets_client

    def load_pilots(self) -> pd.DataFrame:
        return self.sheets.read_df(PILOT_SHEET, PILOT_WORKSHEET)

    def get_available_pilots(self, skill=None, location=None) -> pd.DataFrame:
        df = self.load_pilots()

        # Normalize status and filter available pilots
        df = df[df["status"].str.lower() == "available"]

        if skill:
            df = df[df["skills"].str.contains(skill, case=False, na=False)]

        if location:
            df = df[df["location"].str.contains(location, case=False, na=False)]

        return df

    def update_pilot_status(self, pilot_name: str, new_status: str) -> bool:
        ws = self.sheets.client.open(PILOT_SHEET).worksheet(PILOT_WORKSHEET)
        records = ws.get_all_records()

        for idx, row in enumerate(records, start=2):
            if row["name"].strip().lower() == pilot_name.strip().lower():
                status_col = list(row.keys()).index("status") + 1
                ws.update_cell(idx, status_col, new_status)
                return True

        return False
