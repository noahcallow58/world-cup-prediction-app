import streamlit as st
from tournament.schedule import load_groups

def init_state():
    if "groups" not in st.session_state:
        st.session_state.groups = load_groups()

    # if "predictions" not in st.session_state:
    #     st.session_state.predictions = {}

    if "name" not in st.session_state:
        st.session_state.name = ""

    if "email" not in st.session_state:
        st.session_state.email = ""

    if "access_code" not in st.session_state:
        st.session_state.access_code = ""