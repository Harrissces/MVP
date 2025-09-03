import streamlit as st
import json, os

DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

st.set_page_config(page_title="⚡ TANGEDCO Helper Demo", page_icon="🔌")

st.title("⚡ TANGEDCO Helper - Demo UI")
st.subheader("Helping Chennai Residents with Bills & Power Updates")

# Show all registered users (from bot)
data = load_data()
st.write("### 👥 Registered Consumers")
if data:
    for user, number in data.items():
        st.write(f"🔹 User {user} → Consumer Number: {number}")
else:
    st.info("No consumers registered yet. Use Telegram Bot to add one.")

st.write("### 🔔 Bill Due Reminders")
st.info("Telegram bot will remind customers 7/3/1 days before due date.")

st.write("### 💳 Quick Pay")
st.link_button("Go to TANGEDCO Quick Pay", "https://www.tangedco.org")

st.write("### 🚨 Report Outage")
if st.button("Simulate Outage"):
    st.error("Power outage reported. ETA: 2 hours.")

