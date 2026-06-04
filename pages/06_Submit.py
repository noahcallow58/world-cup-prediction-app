import re
import random
import streamlit as st

from tournament.schedule import load_groups
from tournament.scoring import build_prediction_payload

from services.google_sheets import submit_predictions
from services.state import init_state

init_state()

st.title("Submit Predictions")

st.markdown(
    """
Submit your World Cup predictions.

Only one submission per email is allowed.
Submitting again with the same email will overwrite your previous entry.
"""
)


# ------------------------------------------------------------
# User Inputs
# ------------------------------------------------------------
name = st.text_input(
    "Name", 
    value=st.session_state["name"], 
)

email = st.text_input("Email", 
                      value=st.session_state["email"],
                    #   key="email"
                      )

access_code = st.text_input(
    "Competition Access Code",
    value=st.session_state["access_code"],
    type="password",
)

st.session_state["name"] = name
st.session_state["email"] = email
st.session_state["access_code"] = access_code

# ------------------------------------------------------------
# Development Testing Helper
# ------------------------------------------------------------
if st.secrets["env"]["environment"] == "dev":

    if st.button("Fill Test Predictions"):

        for group in st.session_state.groups:
            for match in group.matches:
                match.home_score = random.randint(0,5)
                match.away_score = random.randint(0,5)

        st.rerun()

# ------------------------------------------------------------
# Validation Helpers
# ------------------------------------------------------------
def valid_email(email: str) -> bool:

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return re.match(pattern, email) is not None


if st.button("Submit Predictions"):

    name = st.session_state.name.strip()
    email = st.session_state.email.strip().lower()
    code = st.session_state.access_code.strip()

    # --------------------------------------------------------
    # Validate name
    # --------------------------------------------------------
    if not name:
        st.error("Please enter your name.")

    # --------------------------------------------------------
    # Validate email
    # --------------------------------------------------------
    elif not valid_email(email):
        st.error("Please enter a valid email address.")

    # --------------------------------------------------------
    # Validate competition access code
    # --------------------------------------------------------
    elif code != st.secrets["competition"]["access_code"]:
        st.error("Invalid competition access code.")

    # --------------------------------------------------------
    # Validate predictions exist
    # --------------------------------------------------------
    # elif "predictions" not in st.session_state:
    #     st.error("No predictions found.")

    else:

        prediction_payload = build_prediction_payload()

        match_exists = any(pred["match_id"] == 104 for pred in prediction_payload)

        if match_exists:
            if prediction_payload is not None:

                submit_predictions(
                    name=name,
                    email=email,
                    predictions=prediction_payload,
                )

                st.success("Predictions submitted successfully!")
        else:
            st.error("Please complete predictions.")