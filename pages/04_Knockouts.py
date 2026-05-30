import streamlit as st
import pandas as pd
from tournament.knockout import resolve_team

st.title("Knockout Stage")

# ------------------------------------------------------------
# 1. Load required data from session
# ------------------------------------------------------------
groups = st.session_state.groups

if "knockout_matches" not in st.session_state:
    st.warning("Knockout fixtures not initialised yet.")
    st.stop()


knockout_matches = st.session_state.knockout_matches

# ------------------------------------------------------------
# 5. Initialise winners state
# ------------------------------------------------------------
if "knockout_winners" not in st.session_state:
    st.session_state.knockout_winners = {}


winners = st.session_state.knockout_winners


# ------------------------------------------------------------
# 6. Render knockout matches
# ------------------------------------------------------------
st.subheader("Knockout Fixtures")

current_round = None

for match in knockout_matches:

    if match.round != current_round:
        current_round = match.round
        st.subheader(current_round)

    state = {
        "group_standings": st.session_state.group_standings,
        "knockout_winners": st.session_state.knockout_winners,
    }

    home_team = resolve_team(match.home_ref, state)
    away_team = resolve_team(match.away_ref, state)
    print(home_team, away_team)

    st.markdown(f"### {home_team} vs {away_team}")

    col1, col2 = st.columns(2)

    key = str(match.match_id)

    home_score = st.number_input(
        f"{home_team}",
        min_value=0,
        step=1,
        key=f"home_{key}",
    )

    away_score = st.number_input(
        f"{away_team}",
        min_value=0,
        step=1,
        key=f"away_{key}",
    )

    match.home_score = home_score
    match.away_score = away_score

    # --------------------------------------------------------
    # Determine winner
    # --------------------------------------------------------
    if home_score is not None and away_score is not None:

        if home_score > away_score:
            winners[f"W{match.match_id}"] = home_team

        elif away_score > home_score:
            winners[f"W{match.match_id}"] = away_team

        else:
            winners[f"W{match.match_id}"] = "TBD (extra time needed)"

    st.divider()


# ------------------------------------------------------------
# 7. Preview bracket progression
# ------------------------------------------------------------
st.subheader("Current Qualified Teams")

st.json(winners)