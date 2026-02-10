import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

class GoogleSheetsClient:
    def __init__(self, creds_path: str):
        creds = Credentials.from_service_account_file(
            creds_path,
            scopes=SCOPES
        )
        self.client = gspread.authorize(creds)

    def read_df(self, sheet_name: str, worksheet: str = "Sheet1") -> pd.DataFrame:
        sheet = self.client.open(sheet_name)
        ws = sheet.worksheet(worksheet)
        data = ws.get_all_records()
        return pd.DataFrame(data)

    def update_cell(self, sheet_name: str, worksheet: str, row: int, col: int, value):
        sheet = self.client.open(sheet_name)
        ws = sheet.worksheet(worksheet)
        ws.update_cell(row, col, value)
