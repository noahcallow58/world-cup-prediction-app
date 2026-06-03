import re
import random
import streamlit as st

from tournament.schedule import load_groups

from services.google_sheets import submit_predictions

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


def build_prediction_payload():

    groups = st.session_state.groups

    if st.secrets["env"]["environment"] == "dev":
        groups = groups[:2]  # Only Groups A and B

    print(groups, st.secrets["env"]["environment"])

    missing = []
    predictions = []

    for group in groups:
        for match in group.matches:

            if not match.is_played():
                missing.append(
                    f"{group.name}: {match.home_team.name} vs {match.away_team.name}"
                )
                continue

            predictions.append({
                "match_id": match.match_id,
                "group": group.name,
                "home_team": match.home_team.name,
                "away_team": match.away_team.name,
                "home_score": match.home_score,
                "away_score": match.away_score,
            })

    if missing:
        st.error("Enter predictions for:\n" + "\n".join(missing))
        return None

    return predictions


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

        if prediction_payload is not None:

            submit_predictions(
                name=name,
                email=email,
                predictions=prediction_payload,
            )

            st.success("Predictions submitted successfully!")