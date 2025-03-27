import streamlit as st
import google.generativeai as gen_ai

# ---- Streamlit Page Configuration ----
st.set_page_config(
    page_title="Niramaya AI Chatbot",
    page_icon="💬",
    layout="centered",
)

# ---- Custom Styling ----
st.markdown("""
    <style>
        /* Body Styling */
        body { background-color: #121212; color: white; }

        /* Centered Title Styling */
        .title-container {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: white;
            background: linear-gradient(90deg, #00D4FF, #00FFA3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 2px 2px 10px rgba(0, 212, 255, 0.5);
            margin-bottom: 20px;
        }

        /* User Message Styling */
        .user-message { 
            background-color: #2A2A2A; 
            color: white; 
            padding: 12px; 
            border-radius: 8px; 
            margin-bottom: 15px;
            border-left: 5px solid #B266FF;  /* Purple left border */
        }

        /* AI Response Styling */
        .ai-message { 
            background-color: #222; 
            border-left: 5px solid #00D4FF;  /* Blue left border */
            color: white; 
            padding: 12px; 
            border-radius: 8px; 
            box-shadow: 2px 2px 5px rgba(0, 212, 255, 0.3); 
            margin-bottom: 15px;
        }

        /* AI Response Header */
        .ai-header {
            font-weight: bold; 
            color: #00D4FF;
            font-size: 18px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 5px;
        }

        /* Horizontal Separator */
        .separator {
            border-top: 1px solid #444; 
            margin: 20px 0;
        }
    </style>
""", unsafe_allow_html=True)

# ---- Google Gemini-Pro API Setup ----
GOOGLE_API_KEY = 'AIzaSyClRWm6773t7l18M4bZAO0P8HM02T-fRqY'
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')

# Function to convert Gemini-Pro roles to Streamlit-friendly roles
def translate_role(user_role):
    return "assistant" if user_role == "model" else user_role

# ---- Initialize Chat Session ----
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# ---- Sidebar Section ----
st.sidebar.write("🔧 Chat Settings")

# Clear Chat Button
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.chat_session = model.start_chat(history=[])
    st.experimental_rerun()

# Warning Message in Sidebar
st.sidebar.warning("⚠️ The chatbot provides AI-generated advice and should not replace professional medical consultation.")

st.sidebar.markdown("<hr>", unsafe_allow_html=True)
        
st.sidebar.markdown("""
            <div style="text-align:center; color:#888888; font-size:12px;">
            <p>🔬 Powered by Niramaya AI</p>            
            <p>👩‍💻 Developed by Team Knit Wits</p>
            </div>   
                    
        """, unsafe_allow_html=True)

# ---- Centered Title with Gradient Styling ----
st.markdown('<div class="title-container">NIRAMAYA AI CHATBOT</div>', unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; font-size: 18px; margin-bottom: 15px;">
        💡 <b>Ask anything about health, skin diseases, and prevention!</b> <br>
        ✨ <i>This chatbot is powered by Google Gemini</i> ✨
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# ---- Display Chat History ----
for message in st.session_state.chat_session.history:
    role = translate_role(message.role)
    message_text = message.parts[0].text
    
    if role == "user":
        st.markdown(f'<div class="user-message"><b>You:</b> {message_text}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-message"><div class="ai-header">NIRAMAYA AI</div>{message_text}</div>', unsafe_allow_html=True)

# ---- User Input ----
user_prompt = st.chat_input("Ask Niramaya AI...")
if user_prompt:
    # Display User Query
    st.markdown(f'<div class="user-message"><b>You:</b> {user_prompt}</div>', unsafe_allow_html=True)

    # Generate AI Response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display AI Response
    st.markdown(f'<div class="ai-message"><div class="ai-header">NIRAMAYA AI</div>{gemini_response.text}</div>', unsafe_allow_html=True)
