import json
import sys
import base64
import requests
import pandas as pd
import streamlit as st

#URL = st.secrets.LimeSurvey.url

headers = {
                "Content-Type": "application/json",
                "connection": "Keep-Alive"
            }

class LimeSurveyAPI:
    def __init__(
            self,
            url,
            session_key,
            survey_id
        ):

            self.url = url
            self.session_key = session_key
            self.survey_id = survey_id

    def export_responses(self):
        req = requests.post(
            url=self.url,
            data=json.dumps({'method':'export_responses', 'params':[self.session_key, self.survey_id, "json", "es", "complete"], 'id': 2}),
            headers=headers
        )
        try:
            result = req.json()['result']
            decodeData = base64.b64decode(result)
            df = pd.DataFrame(json.loads(decodeData)['responses'])
            columnas_prohibidas = [
                "seed",
                "lastpage",
                "startlanguage",
                "submitdate",
                "ipaddr",
                "refurl",
                "startdate",
                "datestamp"
            ]

            return df.drop(columns=columnas_prohibidas)
        except:
            e = sys.exc_info()[0]