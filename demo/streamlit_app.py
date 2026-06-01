# demo/streamlit_app.py

import json

import requests
import streamlit as st


API_URL = st.text_input(
    "API URL",
    "http://localhost:8000/predict",
)

default_payload = {"text": "hello world"}

payload_text = st.text_area(
    "Request JSON",
    value=json.dumps(default_payload, indent=2),
    height=250,
)

if st.button("Send Request"):
    try:
        payload = json.loads(payload_text)

        response = requests.post(
            API_URL,
            json=payload,
            timeout=60,
        )

        st.subheader("Status Code")
        st.code(str(response.status_code))

        st.subheader("Response JSON")
        st.json(response.json())

    except json.JSONDecodeError as e:
        st.error(f"Invalid JSON: {e}")

    except Exception as e:
        st.error(str(e))
