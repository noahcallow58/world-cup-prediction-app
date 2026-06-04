import streamlit as st
from tournament.schedule import load_groups
import pandas as pd

def init_state():
    if "initialised" not in st.session_state:
        st.session_state.initialised = True

        groups, knockouts = load_groups()

        if "groups" not in st.session_state:
            st.session_state.groups = groups

        # if "predictions" not in st.session_state:
        #     st.session_state.predictions = {}

        if "name" not in st.session_state:
            st.session_state.name = ""

        if "email" not in st.session_state:
            st.session_state.email = ""

        if "access_code" not in st.session_state:
            st.session_state.access_code = ""

        if "knockout_matches" not in st.session_state:
            st.session_state.knockout_matches = knockouts

        if "knockout_winners" not in st.session_state:
            st.session_state.knockout_winners = {}

        if "knockout_losers" not in st.session_state:
            st.session_state.knockout_losers = {}

        if "group_standings" not in st.session_state:
            st.session_state.group_standings = {}

        if "group_tiebreakers" not in st.session_state:
            st.session_state.group_tiebreakers = {}

        if "resolved_teams" not in st.session_state:
            st.session_state.resolved_teams = {}  # Format: {match_id_home: "Brazil", match_id_away: "France"}

        # 1. Initialize a reset counter in session state
        if "reset_counter" not in st.session_state:
            st.session_state.reset_counter = 0

        if "knockout_matches" not in st.session_state:
            st.warning("Knockout fixtures not initialised yet.")
            st.stop()

        if "annex_c" not in st.session_state:
            st.session_state.annex_c = pd.read_csv(
                "data/annexC.csv"
            )