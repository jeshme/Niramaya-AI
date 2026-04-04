import streamlit as st
import google.generativeai as gen_ai
import os

# ---- Streamlit Page Configuration ----
st.set_page_config(
    page_title="Niramaya AI Chatbot",
    page_icon="💬",
    layout="centered",
)

# ---- Google Gemini-Pro API Setup ----
GOOGLE_API_KEY = 'AIzaSyDzLx3TvGOOTba1jWlC0FnY5w5mZkJ6lDs'

gen_ai.configure(api_key=GOOGLE_API_KEY)

# ---- Use Stable Model ----
model = gen_ai.GenerativeModel("models/gemini-2.5-flash")

# ---- Initialize Chat Session ----
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# ---- Custom Styling ----
st.markdown("""
    <style>
        body { background-color: #121212; color: white; }

        .title-container {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            background: linear-gradient(90deg, #00D4FF, #00FFA3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
        }

        .user-message { 
            background-color: #2A2A2A; 
            padding: 12px; 
            border-radius: 8px; 
            margin-bottom: 15px;
            border-left: 5px solid #B266FF;
        }

        .ai-message { 
            background-color: #222; 
            border-left: 5px solid #00D4FF;
            padding: 12px; 
            border-radius: 8px; 
            margin-bottom: 15px;
        }

        .ai-header {
            font-weight: bold; 
            color: #00D4FF;
            margin-bottom: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# ---- Sidebar ----
st.sidebar.title("🔧 Settings")

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.chat_session = model.start_chat(history=[])
    st.rerun()

st.sidebar.warning("⚠️ This chatbot is for informational purposes only.")

# ---- Title ----
st.markdown('<div class="title-container">NIRAMAYA AI CHATBOT</div>', unsafe_allow_html=True)

# ---- Display Chat History ----
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else message.role
    text = message.parts[0].text

    if role == "user":
        st.markdown(f'<div class="user-message"><b>You:</b> {text}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-message"><div class="ai-header">NIRAMAYA AI</div>{text}</div>', unsafe_allow_html=True)

# ---- User Input ----
user_prompt = st.chat_input("Ask something...")

if user_prompt:
    # Show user message
    st.markdown(f'<div class="user-message"><b>You:</b> {user_prompt}</div>', unsafe_allow_html=True)

    # Generate response safely
    try:
        response = st.session_state.chat_session.send_message(user_prompt)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"⚠️ Error: {str(e)}"

    # Show bot response
    st.markdown(f'<div class="ai-message"><div class="ai-header">NIRAMAYA AI</div>{bot_reply}</div>', unsafe_allow_html=True)
