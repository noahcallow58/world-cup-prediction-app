import streamlit as st
import json
from services.state import init_state
from tournament.scoring import build_prediction_payload

init_state()

st.title("Predictions Download Page")

# 1. Define your data (the JSON blob)
prediction_payload = build_prediction_payload()
# print(prediction_payload)

match_exists = any(pred["match_id"] == 104 for pred in prediction_payload)

if match_exists:
    if prediction_payload is not None:

        # 2. Convert the dictionary to a JSON string
        # Using indent=4 makes the downloaded file neat and readable
        json_string = json.dumps(prediction_payload, indent=4)

        st.write("Click the button below to download your predictions.")

        # 3. Create the download button
        st.download_button(
            label="Download",
            data=json_string,
            file_name="WC26_predictions.json",
            mime="application/json"
        )
else:
    st.error("Please complete predictions.")