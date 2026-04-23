import os

import requests
import streamlit as st

from core.logger import setup_logger

logger = setup_logger(__name__)

# Streamlit UI Configuration
st.set_page_config(
    page_title="Mental Health AI Support",
    page_icon="💙",
    layout="centered"
)

# API Endpoint Configuration
API_URL = os.getenv("API_URL", "http://localhost:8001/api/v1/predict/")

st.title("💙 Mental Health AI Support")
st.write("How are you feeling today? Share your thoughts below.")

# Sidebar for Configuration/Info
with st.sidebar:
    st.header("Settings")
    api_endpoint = st.text_input("API Endpoint", value=API_URL)
    st.markdown("---")
    st.info("This enterprise-level UI communicates with a decoupled FastAPI backend.")
    if st.button("Check API Status"):
        try:
            # Check the root of the API
            root_url = api_endpoint.split("/api/v1")[0]
            status_res = requests.get(root_url, timeout=5)
            st.write(f"Status: {status_res.status_code}")
            st.json(status_res.json())
        except Exception as e:
            st.error(f"Status check failed: {e}")

user_input = st.text_area("Your Thoughts", placeholder="Type something here...", height=150)

if st.button("Get Support"):
    if user_input.strip():
        with st.spinner("Analyzing with AI..."):
            try:
                # Call the FastAPI backend
                response = requests.post(
                    api_endpoint,
                    json={"text": user_input},
                    timeout=10
                )

                if response.status_code == 200:
                    result = response.json()

                    # Display Prediction Results
                    st.subheader("Analysis Results")
                    col1, col2 = st.columns(2)

                    with col1:
                        risk_level = result["risk"].lower()
                        risk_color = {"low": "green", "medium": "orange", "high": "red"}
                        color = risk_color.get(risk_level, "blue")
                        st.markdown(f"**Risk Level:** :{color}[{result['risk'].upper()}]")
                        st.write(f"**Confidence Score:** {result['score']}")

                    with col2:
                        st.write("**Top Keywords:**")
                        if result["keywords"]:
                            st.write(", ".join(result["keywords"]))
                        else:
                            st.write("None detected.")

                    # Display Response
                    st.subheader("Supportive Message")
                    st.info(result["response"])

                    # Display Resources if high risk
                    if result["resources"]:
                        st.warning("**Crisis Resources:**")
                        st.markdown(result["resources"])

                elif response.status_code == 401:
                    st.error("Authentication Error: The API returned 401 'Not authenticated'.")
                    st.info("This usually means another service is running on this port. We've switched to port 8001. Please restart the backend with the new command.")
                    logger.error(f"401 Authentication Error: {response.text}")

                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
                    logger.error(f"API returned error: {response.status_code}")

            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the API. Is the FastAPI server running?")
                st.info("Run `uvicorn api.main:app --reload` in a separate terminal.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
                logger.error(f"UI Error: {e}")

    else:
        st.warning("Please enter some text before clicking the button.")

st.markdown("---")
st.caption("Disclaimer: This AI tool is for informational and educational purposes only. It is not a substitute for professional mental health advice, diagnosis, or treatment.")
