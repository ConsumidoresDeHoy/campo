import streamlit as st
from datetime import datetime, timedelta
from auth import logout

SESSION_TIMEOUT = timedelta(minutes=30)

def update_activity():
    st.session_state.last_activity = datetime.now()

def check_session_timeout():

    if "authenticated" not in st.session_state:
        return

    if "last_activity" not in st.session_state:
        st.session_state.last_activity = datetime.now()
        return

    elapsed = datetime.now() - st.session_state.last_activity

    if elapsed > SESSION_TIMEOUT:
        st.warning("Sesión expirada por inactividad")
        logout()

    update_activity()