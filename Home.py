import streamlit as st
import json
from streamlit_lottie import st_lottie

# Set Streamlit page layout to wide mode
st.set_page_config(page_title="🔬 Niramaya AI", page_icon="🛡️", layout="wide")

def load_lottiefile(filepath: str):
    with open(filepath, encoding='utf-8') as f:
        return json.load(f)

# ---- DARK MODE STYLING ----
dark_theme = """
    <style>
        body { background-color: #121212; color: white; }
        .stTextInput, .stSelectbox, .stButton>button { background-color: #333; color: white; }
        .stImage>img { border-radius: 10px; }
        .info-box { 
            background-color: #1E1E1E; 
            padding: 30px; 
            border-radius: 12px; 
            margin-bottom: 35px; 
            border: 1px solid #444;
            line-height: 1.8;
        }
        .container-box { 
            text-align: center; 
            padding: 30px; 
            background-color: #1E1E1E; 
            border-radius: 12px; 
            color: #EEEEEE; 
            font-size: 18px;
            line-height: 1.8;
            margin: auto;
            width: 85%;
        }
        h3 { color: #00bfff; text-align: center; }
    </style>
"""
st.markdown(dark_theme, unsafe_allow_html=True)

# Load Lottie Animation from Local File

ge_ai = load_lottiefile("./resources/Home/gemini-ani.json")
intro = load_lottiefile("./resources/Home/intro-ani.json")
ml = load_lottiefile("./resources/Home/ml-ani.json")
dl = load_lottiefile("./resources/Home/dl-ani.json")


# ---- TITLE ----
st.markdown("<h1 style='text-align:center;'><b>Niramaya AI</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:#BBBBBB;'>Your AI Health Companion</h4>", unsafe_allow_html=True)
c1,c2,c3 = st.columns([1,1,1])
with c2:
    st_lottie(intro, speed=1, width=400, height=400)

# ---- ABOUT NIRAMAYA ----
st.markdown("""
    <div class="container-box">
        <p>
        <b>Niramaya AI</b> is a cutting-edge health assistant designed to leverage <b>artificial intelligence and deep learning</b> for fast and accurate medical insights.  
        It enables users to <b>analyze skin conditions, track asthma risks, and receive AI-powered health recommendations</b>.  
        Built on state-of-the-art machine learning models, Niramaya ensures <b>accessibility, precision, and ease of use</b>, making proactive healthcare available to everyone.  
        </p>
    </div>
""", unsafe_allow_html=True)

# ---- KEY FEATURES ----
st.markdown("<h2 style='text-align:center;'>🚀 <b>Key Features of Niramaya AI</b></h2>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #444;'>", unsafe_allow_html=True)

c_1,c_2 = st.columns([2,1])
# Feature 1: Skin Disease Detection
with c_1:
    st.markdown("""
    <div class="info-box">
        <h3>📷 AI-Powered Skin Disease Detection</h3>
        <p>
        <b>Concerned about a skin condition?</b> Niramaya AI allows users to <b>upload or capture an image</b> of their skin issue for instant analysis.  
        Using a <b>deep-learning-based detection model</b>, it identifies potential conditions such as <b>acne, eczema, fungal infections, or even early signs of skin cancer.</b>  
        It provides users with a <b>preliminary diagnosis, possible causes, symptoms, and recommended treatments</b>, ensuring early detection and informed decision-making.  
        With AI-driven accuracy, it helps bridge the gap between suspicion and medical consultation.  
        </p>
    </div>
""", unsafe_allow_html=True)
    
with c_2:

    st_lottie(dl, speed=1, width=300, height=300)

c_11,c_22 = st.columns([1,2])

with c_11:
    st_lottie(ml, speed=1, width=300, height=300)

with c_22:
# Feature 2: Asthma Risk Assessment
    st.markdown("""
    <div class="info-box">
        <h3>🌬️ AI-Based Asthma Risk Evaluation</h3>
        <p>
        Struggling with <b>shortness of breath, wheezing, or persistent coughing?</b>  
        Niramaya’s AI-powered <b>asthma risk assessment</b> evaluates symptoms, medical history, and environmental factors to determine the <b>probability of asthma</b>.  
        The AI generates a <b>risk score</b> based on the user's input and provides <b>early warnings</b>, allowing timely intervention before symptoms escalate.  
        Users also receive <b>lifestyle recommendations, trigger avoidance tips, and emergency response guidance</b> to manage their respiratory health effectively.  
        </p>
    </div>
""", unsafe_allow_html=True)

c_111,c_222 = st.columns([2,1])

with c_111:
# Feature 3: AI Chatbot for Health Assistance
    st.markdown("""
    <div class="info-box">
        <h3>🤖 24/7 AI Health Chatbot</h3>
        <p>
        Have health-related questions? Niramaya’s <b>AI-powered chatbot</b> is available 24/7 to assist with medical queries.  
        It provides insights on <b>common diseases, symptoms, medications, treatments, and general health concerns</b> in real-time.  
        With a knowledge base trained on <b>medical research and expert guidelines</b>, the chatbot ensures <b>accurate and evidence-based responses</b>.  
        Whether you're looking for quick advice or detailed symptom analysis, Niramaya AI is always ready to help.  
        </p>
    </div>
""", unsafe_allow_html=True)
    
with c_222:
    st_lottie(ge_ai, speed=1, width=300, height=300)

# ---- HOW NIRAMAYA AI WORKS ----
st.markdown("<h2 style='text-align:center;'>⚙️ <b>How Niramaya AI Works</b></h2>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #444;'>", unsafe_allow_html=True)

st.markdown("""
    <div class="container-box">
        <p> 🧠 <b>AI-Driven Technology:</b> Niramaya AI integrates <b>machine learning and deep neural networks</b> to provide accurate and reliable health insights.  </p>
        <p> 📊 <b>Advanced Medical Models:</b> The platform is powered by specialized AI models for <b>skin disease detection</b> and <b>asthma risk assessment</b>.  </p>
        <p> 🔬 <b>Trained on Medical Data:</b> The models have been trained using extensive datasets of <b>verified medical conditions</b> for precise predictions.  </p>
        <p> 🤖 <b>Powered by Google Gemini:</b> The chatbot utilizes <b>Google Gemini AI</b> to deliver fast and reliable health guidance, ensuring up-to-date information.  
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid #444;'>", unsafe_allow_html=True)

st.markdown("""
            <div style="text-align:center; color:#888888; font-size:12px;">
            <p>🔬 Powered by Niramaya AI</p>            
            <p>👩‍💻 Developed by Team Knit Wits</p>
            </div>   
                    
        """, unsafe_allow_html=True)
            