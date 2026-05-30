import streamlit as st
from tournament.schedule import load_groups

def init_state():

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

    if "group_standings" not in st.session_state:
        st.session_state.group_standings = {}