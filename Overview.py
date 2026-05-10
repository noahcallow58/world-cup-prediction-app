import streamlit as st
from services.state import init_state

init_state()

st.set_page_config(
    page_title="World Cup Charity Challenge",
    page_icon="",
    layout="wide",
)

st.title("World Cup Charity Challenge")

st.markdown(
    """
Welcome to the 2026 World Cup Prediction Challenge!

Use the sidebar to navigate between:
- Group stage predictions
- Knockout predictions
- Leaderboard
- Rules

Submit your predictions before the tournament starts.
"""
)

st.divider()

st.markdown("## How It Works")

st.markdown(
    """
- Predict every World Cup match
- Earn points for correct results and scorelines
- Group standings update automatically
- Leaderboard updates throughout the tournament
"""
)

st.divider()

st.info(
    "Predictions are currently stored locally in session state."
)