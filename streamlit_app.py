# streamlit_app.py

import streamlit as st
import requests

st.set_page_config(page_title="Calendar Bot 🤖", layout="centered")

st.title("📅 AI Calendar Booking Assistant")
st.caption("Ask me to book a meeting, and I’ll handle the rest.")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Book a meeting...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        response = requests.post("https://calendar-booking-ai-agent-production.up.railway.app/chat", json={"message": user_input})
        if response.status_code == 200:
            data = response.json()
            final_answer = data.get("final_answer", "✅ Done.")
            steps = data.get("steps", [])

            # Format steps into a readable trace
            reasoning = ""
            for i, step in enumerate(steps, start=1):
                reasoning += (
                    f"**Step {i}:**\n"
                    f"🔧 **Action**: `{step['tool']}`\n"
                    f"📥 **Input**: `{step['tool_input']}`\n"
                    f"📤 **Observation**: {step['observation']}\n\n"
                )

            bot_reply = reasoning + f"✅ **Final Answer**: {final_answer}"

        else:
            bot_reply = "❌ Error: " + response.text
    except Exception as e:
        bot_reply = f"🚫 Exception: {str(e)}"

    st.session_state.messages.append({"role": "bot", "content": bot_reply})

# Display chat
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])
