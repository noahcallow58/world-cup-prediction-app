import json
from datetime import datetime

import gspread
import streamlit as st

from google.oauth2.service_account import Credentials


# ------------------------------------------------------------
# Google Sheets authentication
# ------------------------------------------------------------
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPES,
)

client = gspread.authorize(creds)

sheet = client.open("world-cup-predictions").sheet1


# ------------------------------------------------------------
# Submission logic
# ------------------------------------------------------------
def submit_predictions(
    name: str,
    email: str,
    predictions: dict,
):

    timestamp = datetime.utcnow().isoformat()

    predictions_json = json.dumps(predictions)

    all_rows = sheet.get_all_values()

    # --------------------------------------------------------
    # Check for existing email
    # --------------------------------------------------------
    existing_row_index = None

    # Assume:
    # Row 1 = headers
    #
    # Col A = Timestamp
    # Col B = Name
    # Col C = Email
    # Col D = Predictions

    for i, row in enumerate(all_rows[1:], start=2):

        if len(row) < 3:
            continue

        existing_email = row[2].strip().lower()

        if existing_email == email:

            existing_row_index = i
            break

    # --------------------------------------------------------
    # Update existing row
    # --------------------------------------------------------
    if existing_row_index is not None:

        sheet.update(
            f"A{existing_row_index}:D{existing_row_index}",
            [[
                timestamp,
                name,
                email,
                predictions_json,
            ]]
        )

    # --------------------------------------------------------
    # Append new row
    # --------------------------------------------------------
    else:

        sheet.append_row([
            timestamp,
            name,
            email,
            predictions_json,
        ])