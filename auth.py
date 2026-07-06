import streamlit as st
import requests
import json

URL = st.secrets.LimeSurvey.url
KOBOTOOLBOX_TOKEN = st.secrets.KOBO_TOKEN.token

class LoginError(Exception):
    pass

def detect_platform(user):
    if "@" in user:
        return "kobo"
    else:
        return "limesurvey"

def login_limesurvey(username, password):
    payload = {
            "method": "get_session_key",
            "params": [
                username,
                password
            ],
            "id": 1
        }
    
    headers = {
            "Content-Type": "application/json",
            "connection": "Keep-Alive"
    }

    req = requests.post(
        url = URL,
        data=json.dumps(payload),
        headers = headers
    )
    result = req.json()
    session_key = result.get('result')
    #print(result)
    if not session_key:
        raise LoginError(session_key)
    
    if "Invalid" in session_key:
        raise LoginError(session_key)
    
    if "excedido" in session_key:
        raise LoginError(session_key)

    st.session_state.authenticated = True
    st.session_state.platform = "limesurvey"
    st.session_state.username = username
    st.session_state.session_key = session_key

    return True

def login_kobo(username, password):

    users = st.secrets["auth"]["users"]

    for user in users:
        if (user["username"] == username and user["password"] == password):
            st.session_state.authenticated = True
            st.session_state.platform = "kobo"
            st.session_state.username = username
            st.session_state.token = KOBOTOOLBOX_TOKEN

            return True

    raise LoginError("Invalid user name or password.")

def login(username, password):

    if not username or not password:
        raise LoginError("Please enter your username and password.")

    platform = detect_platform(username)

    if platform == "limesurvey":
        return login_limesurvey(username, password)

    return login_kobo(username, password)



def release_ls_session():

    if "session_key" not in st.session_state:
        return

    payload = {
        "method": "release_session_key",
        "params": [
            st.session_state.session_key
        ],
        "id": 99
    }

    try:
        requests.post(
            URL,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "connection": "Keep-Alive"
            }
        )

    except Exception:
        pass

def logout():

    if("platform" in st.session_state and st.session_state.platform == "limesurvey"):
        release_ls_session()
    keys = list(st.session_state.keys())

    for key in keys:
        del st.session_state[key]
    st.rerun()