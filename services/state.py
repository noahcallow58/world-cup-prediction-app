import streamlit as st

def init_state():

    if "predictions" not in st.session_state:
        st.session_state.predictions = {}

    if "name" not in st.session_state:
        st.session_state.name = ""

    if "email" not in st.session_state:
        st.session_state.email = ""

    if "access_code" not in st.session_state:
        st.session_state.access_code = ""