import streamlit as st
import google.generativeai as gen_ai
import os

# ---- Streamlit Page Configuration ----
st.set_page_config(
    page_title="Niramaya AI Chatbot",
    page_icon="💬",
    layout="centered",
)

# ---- Get API Key (Supports BOTH local .env & Streamlit secrets) ----
GOOGLE_API_KEY = None

# 1. Try Streamlit secrets (for deployment)
if "GOOGLE_API_KEY" in st.secrets:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# 2. Fallback to local .env (for development)
else:
    from dotenv import load_dotenv
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ---- Error if key missing ----
if not GOOGLE_API_KEY:
    st.error("❌ API Key not found! Add it in .env (local) or secrets.toml (deploy)")
    st.stop()

# ---- Configure Gemini ----
gen_ai.configure(api_key=GOOGLE_API_KEY)

model = gen_ai.GenerativeModel("models/gemini-2.5-flash")

# ---- Initialize Chat Session ----
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# ---- UI Styling ----
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

# ---- Display Chat ----
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else message.role
    text = message.parts[0].text

    if role == "user":
        st.markdown(f'<div class="user-message"><b>You:</b> {text}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-message"><div class="ai-header">NIRAMAYA AI</div>{text}</div>', unsafe_allow_html=True)

# ---- Input ----
user_prompt = st.chat_input("Ask something...")

if user_prompt:
    st.markdown(f'<div class="user-message"><b>You:</b> {user_prompt}</div>', unsafe_allow_html=True)

    try:
        response = st.session_state.chat_session.send_message(user_prompt)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"⚠️ Error: {str(e)}"

    st.markdown(f'<div class="ai-message"><div class="ai-header">NIRAMAYA AI</div>{bot_reply}</div>', unsafe_allow_html=True)
