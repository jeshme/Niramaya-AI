import streamlit as st
import csv
import ssl
import smtplib
from email.message import EmailMessage
import datetime
import json
from streamlit_lottie import st_lottie

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Niramaya Asthma Tracker", page_icon="🩺", layout="wide")

# ---- DARK MODE STYLING ----
dark_bg = """
    <style>
        body { background-color: #121212; color: white; }
        .stImage>img { border-radius: 10px; }
        .info-box { background-color: #1E1E1E; padding: 20px; border-radius: 10px; color: white; }
        .container-box { 
            text-align: center; 
            padding: 20px; 
            background-color: #1E1E1E; 
            border-radius: 10px; 
            color: #EEEEEE; 
            font-size: 18px;
            line-height: 1.6;
            margin: auto;
            width: 80%;
        }
    </style>
"""
st.markdown(dark_bg, unsafe_allow_html=True)

# ---- LOAD LOTTIE ANIMATION ----
def load_lottiefile(filepath: str):
    with open(filepath, encoding='utf-8') as f:
        return json.load(f)

lottie_animation = load_lottiefile("./resources/Asthma/asthma-animation.json")

# ---- SIDEBAR: USER NAME INPUT ----
st.sidebar.markdown("## 🏥 Enter Your Name")
user_name = st.sidebar.text_input("Name")

# ---- DISPLAY INTRODUCTION UNTIL NAME IS ENTERED ----
if not user_name:
    st.markdown("<h2 style='text-align:center;'>🩺 Niramaya Asthma Tracker</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; color:#BBBBBB;'>Monitor your respiratory health</h4>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #444;'>", unsafe_allow_html=True)

    with st.container():
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st_lottie(lottie_animation, speed=1, width=250, height=250)

    st.markdown("""
        <div class="container-box">
            <p>
            <b>Niramaya Asthma Tracker</b> is an advanced AI-powered tool designed to help individuals 
            monitor their respiratory health. By regularly tracking symptoms, users can detect early signs 
            of an asthma attack and take necessary precautions. Our system calculates risk levels based on 
            your inputs and alerts medical professionals if necessary.
            </p>
            <p>
            Enter your name in the sidebar to begin tracking your symptoms and ensure timely intervention 
            for better respiratory health.
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# ---- SYMPTOM WEIGHTS ----
feature_weights = {
    'Pains': 0.161170,
    'Tiredness': 0.147855,
    'Runny-Nose': 0.146093,
    'Dry-Cough': 0.140978,
    'Nasal-Congestion': 0.140762,
    'Sore-Throat': 0.131730,
    'Difficulty-in-Breathing': 0.131413
}

# ---- EMAIL FUNCTION ----
def email_alert(date, severity_percentage, symptoms, user_name):
    email_sender = "99220040285@klu.ac.in"
    email_password = "lema ezno hqyo wopk"
    email_recipient = "hfutureready@gmail.com"
    subject = f" Niramaya Asthma Alert for {user_name} - {date}"
    body = f"""
Dear Doctor,

A potential risk of an Asthma exacerbation has been detected for {user_name}.

Symptoms reported:
- Tiredness: {"Yes" if symptoms.get('Tiredness', 0) == 1 else "No"}
- Dry Cough: {"Yes" if symptoms.get('Dry-Cough', 0) == 1 else "No"}
- Difficulty in Breathing: {"Yes" if symptoms.get('Difficulty-in-Breathing', 0) == 1 else "No"}
- Sore Throat: {"Yes" if symptoms.get('Sore-Throat', 0) == 1 else "No"}
- Pains: {"Yes" if symptoms.get('Pains', 0) == 1 else "No"}
- Nasal Congestion: {"Yes" if symptoms.get('Nasal-Congestion', 0) == 1 else "No"}
- Runny Nose: {"Yes" if symptoms.get('Runny-Nose', 0) == 1 else "No"}

Date: {date}
Severity: {round(severity_percentage, 2)}%

Please review the patient’s condition and provide necessary guidance.

Best regards,  
Niramaya Asthma Alert System
"""

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_recipient
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_recipient, em.as_string())

# ---- SEVERITY CALCULATION FUNCTION ----
def calculate_severity_percentage(symptoms):
    severity = sum(feature_weights[symptom] * value for symptom, value in symptoms.items())
    return severity * 100

# ---- UI FOR SYMPTOM INPUT ----
st.markdown("<h2 style='text-align:center;'>🩺 Niramaya Asthma Tracker</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:#BBBBBB;'>Monitor your respiratory health</h4>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #444;'>", unsafe_allow_html=True)

st.info("Select your symptoms from the options below.")

col1, col2, col3 = st.columns(3)

with col1:
    tiredness = st.selectbox('Tiredness', ['- Select -', 'Yes', 'No'])
    dry_cough = st.selectbox('Dry Cough', ['- Select -', 'Yes', 'No'])
    difficulty_breathing = st.selectbox('Difficulty in Breathing', ['- Select -', 'Yes', 'No'])
with col2:
    sore_throat = st.selectbox('Sore Throat', ['- Select -', 'Yes', 'No'])
    pains = st.selectbox('Pains', ['- Select -', 'Yes', 'No'])
with col3:
    nasal_congestion = st.selectbox('Nasal Congestion', ['- Select -', 'Yes', 'No'])
    runny_nose = st.selectbox('Runny Nose', ['- Select -', 'Yes', 'No'])

# Convert user input to binary values
user_symptoms = {symptom: 1 if value == 'Yes' else 0 for symptom, value in 
                 zip(feature_weights.keys(), [tiredness, dry_cough, difficulty_breathing, sore_throat, pains, nasal_congestion, runny_nose])}

# ---- BUTTON FOR PREDICTION ----
if st.button('🔍 Predict Severity'):
    severity_percentage = calculate_severity_percentage(user_symptoms)
    
    if severity_percentage > 60:
        st.error(f'⚠️ {severity_percentage:.2f}% - High risk of Asthma attack!.')

        with st.expander("🚑 Precautionary Steps (Click to Expand)"):
            st.markdown("""
                <div style="background-color:#1E1E1E; padding:15px; border-radius:10px; color:white;">
                    <h4>✅ What to Do:</h4>
                    <ul>
                        <li>Use your prescribed inhaler immediately.</li>
                        <li>Stay calm and practice controlled breathing.</li>
                        <li>Seek fresh air or a well-ventilated area.</li>
                        <li>Drink warm fluids to ease throat irritation.</li>
                    </ul>
                    <h4>🚫 What to Avoid:</h4>
                    <ul>
                        <li>Do not expose yourself to dust, smoke, or strong odors.</li>
                        <li>Avoid intense physical activity until symptoms subside.</li>
                        <li>Do not take medications that haven't been prescribed.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

        st.info("An alert has been sending to your healthcare provider.")
        email_alert(datetime.date.today().strftime("%Y-%m-%d"), severity_percentage, user_symptoms, user_name)
        st.success('📩 Email sent successfully!')
    else:
        st.info(f'✅ {severity_percentage:.2f}% - Low risk of Asthma attack.')
    
    st.markdown("""
            <div style="text-align:center; color:#888888; font-size:12px;">
            <p>🔬 Powered by Niramaya AI</p>            
            <p>👩‍💻 Developed by Team Knit Wits</p>
            </div>   
                    
        """, unsafe_allow_html=True)
