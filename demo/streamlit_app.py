# demo/streamlit_app.py

import json
import os

import requests
import streamlit as st


API_URL = st.text_input(
    "API URL",
    os.environ.get("API_URL", "http://localhost:8000/predict"),
)

default_payload = {
    "longitude": -6.05,
    "latitude": 4.97,
    "B2": 0.036,
    "B3": 0.054,
    "B4": 0.042,
    "B5": 0.096,
    "B6": 0.211,
    "B7": 0.242,
    "B8": 0.240,
    "B8A": 0.265,
    "B11": 0.125,
    "B12": 0.062,
    "VV": -7.65,
    "VH": -14.51,
}

payload_text = st.text_area(
    "Request JSON",
    value=json.dumps(default_payload, indent=2),
    height=420,
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
