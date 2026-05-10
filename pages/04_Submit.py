import re

import streamlit as st

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
# Validation Helpers
# ------------------------------------------------------------
def valid_email(email: str) -> bool:

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return re.match(pattern, email) is not None


def build_prediction_payload():

    predictions = {}

    for key, value in st.session_state.predictions.items():

        # Expected:
        # "22_home"
        # "22_away"

        match_id, side = key.split("_")

        if match_id not in predictions:
            predictions[match_id] = {}

        predictions[match_id][side] = value

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
    elif "predictions" not in st.session_state:
        st.error("No predictions found.")

    else:

        prediction_payload = build_prediction_payload()

        # ----------------------------------------------------
        # Validate completeness
        # ----------------------------------------------------
        incomplete = []

        for match_id, scores in prediction_payload.items():

            if (
                "home" not in scores
                or "away" not in scores
                or scores["home"] is None
                or scores["away"] is None
            ):
                incomplete.append(match_id)

        if incomplete:

            st.error(
                f"Incomplete predictions for matches: {', '.join(incomplete)}"
            )

        else:

            submit_predictions(
                name=name,
                email=email,
                predictions=prediction_payload,
            )

            st.success("Predictions submitted successfully!")