from auth import login, logout, LoginError
from session_manager import check_session_timeout
from ls_api import LimeSurveyAPI

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

#================================================================================
URL = st.secrets.LimeSurvey.url
#================================================================================
st.set_page_config(
    #page_title="Realtime Portal", [LimeSurvey]
    #url="http://encuestas.perceptionssurveys.com/index.php/admin/remotecontrol"
    layout="wide"
)

#ensure_directories()
check_session_timeout()

if "authenticated" not in st.session_state or not st.session_state.authenticated:

    st.title("Evaluación de Personal de Campo")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")


    if st.button("Ingresar"):
        try:
            login(username, password)
            st.rerun()
        except LoginError as e:
            st.error(str(e))

    st.stop()

#================================================================================
def plot_puntos_por_proyecto(data, project):
    puntos = data.sort_values(by='Puntos', ascending=False)

    plt.figure(figsize=(10, 6))
    plt.bar(puntos['ENTREVISTADOR'], puntos['Puntos'], color='skyblue')
    plt.title('Puntos por Proyecto: ' + project)
    plt.xlabel('Encuestadores')
    plt.ylabel('Total de Puntos')
    plt.xticks(rotation=45)
    for i, value in enumerate(puntos['Puntos']):
        plt.text(i, value, str(value), ha='center')
    plt.tight_layout()
    st.pyplot(plt)

#================================================================================

col1, col2 = st.columns([8, 1])
with col1:
    st.title("EVALUACIÓN")
    st.write(f"User: {st.session_state.username}")
with col2:
    if st.button("Logout"):
        logout()

if st.session_state.platform == "limesurvey":
    project_label = "Survey ID"
    holder = "112233"
else:
    project_label = "Form ID"
    holder = "abcXYZ123A4F"

project_id = st.text_input(project_label, placeholder=holder)

if st.button("Submit"):

    if not project_id:
        st.warning("Enter an ID")
        st.stop()

    if st.session_state.platform == "limesurvey" and int(project_id) in range(1,999999):

            api = LimeSurveyAPI(
                url=URL,
                session_key=st.session_state.session_key,
                survey_id=project_id
            )

            with st.spinner("Loading database..."):
                data = api.export_responses()
    else:
        st.error("Invalid ID")
        st.stop()


#===========================================================================
    
    #st.stop()
    atributos = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10']
    data[atributos] = data[atributos].astype(str).astype(int)
    data['Puntos'] = data[atributos].sum(axis=1)
    data['PROYECTO'] = data['PROYECTO'].str.rstrip()
    data['PROYECTO'] = data['PROYECTO'].str.upper()
    proyectos = data['PROYECTO'].unique()
    #st.write(data)
    #st.stop()
    for proyecto in proyectos:
        datatemp = data[data['PROYECTO'] == proyecto]
        plot_puntos_por_proyecto(datatemp, proyecto)
        #st.write(datatemp)

#===========================================================================