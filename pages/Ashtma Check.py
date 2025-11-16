import streamlit as st
import google.generativeai as gen_ai
import os
from google.api_core.exceptions import ResourceExhausted

# ---- Load Gemini API Key from Environment ----
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY not found in environment variables. Please set it before running the app.")
else:
    gen_ai.configure(api_key=GOOGLE_API_KEY)

# ---- Select Gemini Model ----
model = gen_ai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')

# ---- Streamlit Page Configuration ----
st.set_page_config(
    page_title="Niramaya AI Chatbot",
    page_icon="💬",
    layout="centered",
)

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
            text-shadow: 2px 2px 10px rgba(0, 212, 255, 0.5);
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
            box-shadow: 2px 2px 5px rgba(0, 212, 255, 0.3);
            margin-bottom: 15px;
        }

        .ai-header {
            font-weight: bold; 
            color: #00D4FF;
            font-size: 18px;
            text-transform: uppercase;
            margin-bottom: 5px;
        }

        .separator {
            border-top: 1px solid #444; 
            margin: 20px 0;
        }
    </style>
""", unsafe_allow_html=True)

# ---- Function to Convert Roles ----
def translate_role(user_role):
    return "assistant" if user_role == "model" else user_role

# ---- Initialize Chat Session ----
if "chat_session" not in st.session_state and GOOGLE_API_KEY:
    st.session_state.chat_session = model.start_chat(history=[])

# ---- Sidebar ----
st.sidebar.write("🔧 Chat Settings")

if st.sidebar.button("🗑️ Clear Chat") and GOOGLE_API_KEY:
    st.session_state.chat_session = model.start_chat(history=[])
    st.experimental_rerun()

st.sidebar.warning("⚠️ AI-generated advice. Not a substitute for a medical professional.")
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown("""
    <div style="text-align:center; color:#888; font-size:12px;">
        <p>🔬 Powered by Niramaya AI</p>
        <p>👩‍💻 Developed by Team Knit Wits</p>
    </div>
""", unsafe_allow_html=True)

# ---- Title ----
st.markdown('<div class="title-container">NIRAMAYA AI CHATBOT</div>', unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; font-size: 18px; margin-bottom: 15px;">
        💡 <b>Ask anything about health, skin diseases, and prevention!</b> <br>
        ✨ <i>This chatbot is powered by Google Gemini</i> ✨
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# ---- Display Chat History ----
if GOOGLE_API_KEY:
    for message in st.session_state.chat_session.history:
        role = translate_role(message.role)
        message_text = message.parts[0].text

        if role == "user":
            st.markdown(f'<div class="user-message"><b>You:</b> {message_text}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-message"><div class="ai-header">NIRAMAYA AI</div>{message_text}</div>', unsafe_allow_html=True)

# ---- User Input ----
if GOOGLE_API_KEY:
    user_prompt = st.chat_input("Ask Niramaya AI...")

    if user_prompt:
        st.markdown(f'<div class="user-message"><b>You:</b> {user_prompt}</div>', unsafe_allow_html=True)

        try:
            # Send only last 5 messages to reduce resource usage
            last_history = st.session_state.chat_session.history[-5:]
            chat_session_limited = model.start_chat(history=last_history)
            gemini_response = chat_session_limited.send_message(user_prompt)

            st.markdown(
                f'<div class="ai-message"><div class="ai-header">NIRAMAYA AI</div>{gemini_response.text}</div>',
                unsafe_allow_html=True
            )

            # Update main chat session history with new message
            st.session_state.chat_session.history.append(
                gemini_response._proto  # Keep same format as original
            )

        except ResourceExhausted:
            st.error("⚠️ Gemini API quota exceeded or resource limit reached. Please try again later.")
        except Exception as e:
            st.error(f"⚠️ An unexpected error occurred: {e}")
