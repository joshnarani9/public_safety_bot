import streamlit as st
import requests
import pandas as pd
import os


# Page config
st.set_page_config(page_title="🚨 Public Safety Bot", layout="wide")
st.markdown("<h1 style='text-align: center; color: red;'>🚨 Indiana Public Safety Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Chat with the bot to report hazards, get alerts, or ask for help.</p>", unsafe_allow_html=True)
st.markdown("---")

# 🔐 Load FastAPI backend URL from environment variable
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")  # fallback for local dev

# Session state for user message
if "user_message" not in st.session_state:
    st.session_state.user_message = ""

# 🎯 User ID (shared across tabs)
with st.sidebar:
    st.image("img.png", width=80)
    user_id = st.text_input("👤 Enter Your ID", value="user123")
    st.markdown("---")
    st.info("Use the same ID across features to sync your reports.")

# Tabs
tabs = st.tabs(["💬 Chat with Bot", "📋 My Hazard Reports", "📍 Location Update"])

# 💬 Chat Tab
with tabs[0]:
    st.markdown("### 💬 Talk to the Safety Bot")
    user_message = st.text_area("Type your message", key="user_message", placeholder="e.g., There's a fire near 5th Avenue.")

    if st.button("🚀 Send Message"):
        if user_message.strip():
            with st.spinner("Analyzing your message..."):
                try:
                    response = requests.post(
                        f"{FASTAPI_URL}/chat",
                        json={"message": user_message, "user_id": user_id}
                    )
                    if response.status_code == 200:
                        res = response.json()
                        st.success(f"🧠 Intent: {res['intent']}")
                        st.info(f"💬 Bot: {res['response']}")
                        st.caption(f"📨 Original: {res.get('user_input', '')}")
                        if res["data"]:
                            st.write("📍 Extracted Info:")
                            st.json(res["data"])
                    else:
                        st.error("❌ Failed to get a response from the bot.")
                except Exception as e:
                    st.error(f"💥 Error: {str(e)}")
        else:
            st.warning("✏️ Please enter a message first.")

# 📋 Reports Tab
with tabs[1]:
    st.markdown("### 📋 Your Past Hazard Reports")
    try:
        reports = requests.get(f"{FASTAPI_URL}/reports/{user_id}")
        if reports.status_code == 200:
            data = reports.json()
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("📭 No reports found for this ID.")
        else:
            st.error("❌ Could not fetch reports.")
    except Exception as e:
        st.error(f"💥 Error: {str(e)}")

# 📍 Location Update Tab
with tabs[2]:
    st.markdown("### 📍 Update Your Location")

    new_location = st.text_input("Enter New Location")
    
    if st.button("🔁 Update Location"):
        try:
            res = requests.post(
                f"{FASTAPI_URL}/location",
                json={"location": new_location, "user_id": user_id}
            )
            if res.status_code == 200:
                st.success(res.json()["message"])
            else:
                st.error("❌ Could not update location.")
        except Exception as e:
            st.error(f"💥 Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 14px;'>👷‍♀️ Built for the Civic Tech Hackathon 2025</p>", unsafe_allow_html=True)
