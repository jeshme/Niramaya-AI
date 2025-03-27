import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import pandas as pd
from streamlit_lottie import st_lottie
import json

# Load Data and Model
data = pd.read_csv('./resources/Skin Cancer/data.csv')
model = tf.keras.models.load_model('./resources/Skin Cancer/model.h5')

# Define Constants
IMAGE_SIZE = (32, 32)
diseases = ['Actinic keratoses', 'Basal cell carcinoma', 'Benign keratosis', 'Dermatofibroma', 
            'Melanoma', 'Melanocytic nevi', 'Vascular lesions']

# Dark Mode Styling
st.set_page_config(page_title="Niramaya Skin Check", page_icon="🩺", layout="wide")

dark_bg = """
    <style>
        body { background-color: #121212; color: white; }
        .stTextInput, .stFileUploader, .stButton>button, .stCameraInput>button { background-color: #333; color: white; }
        .stImage>img { border-radius: 10px; }
        .info-box { background-color: #1E1E1E; padding: 20px; border-radius: 10px; color: white; }
        .stRadio>label { color: white; }
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

# Load Lottie Animation from Local File
def load_lottiefile(filepath: str):
    with open(filepath, encoding='utf-8') as f:
        return json.load(f)


lottie_animation = load_lottiefile("./resources/Skin Cancer/skin-animation.json")

# ---- SIDEBAR: USER SELECTION ----
st.sidebar.markdown("## 🏥 Choose Input Method")
input_choice = st.sidebar.selectbox("", [" - select - ", "Upload Image", "Capture Image"])

# ---- TITLE ----
st.markdown("""
    <h2 style="text-align:center;">🩺 Niramaya Skin Check</h2>
    <h4 style="text-align:center; color:#BBBBBB;">AI-powered early diagnosis</h4>
    <hr style="border: 1px solid #444;">
""", unsafe_allow_html=True)

# ---- DISPLAY INTRODUCTION UNTIL IMAGE IS UPLOADED ----
if input_choice == " - select - ":
    with st.container():
        col1, col2, col3 = st.columns([1, 1, 1])  # Center alignment
        with col2:
            st_lottie(lottie_animation, speed=1, width=250, height=250)

    st.markdown("""
        <div class="container-box">
            <p>
            <b>Niramaya</b> is an AI-powered health platform designed for early disease detection and prevention.
            Using advanced deep learning models, Niramaya analyzes skin images to identify potential conditions,
            providing users with quick and reliable insights. With a simple image upload or camera capture,
            users can detect skin diseases, empowering them to take early action toward better health.
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# ---- IMAGE UPLOAD OR CAMERA INPUT ----
image_source = None
if input_choice == "Upload Image":
    uploaded_file = st.sidebar.file_uploader("Upload a clear skin image", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        image_source = uploaded_file
elif input_choice == "Capture Image":
    camera_image = st.camera_input("Capture an image")
    if camera_image is not None:
        image_source = camera_image

# ---- SHOW MESSAGE IF NO IMAGE SELECTED ----
if image_source is None:
    st.markdown("<h4 style='text-align:center;'>Upload or capture an image to proceed.</h4>", unsafe_allow_html=True)
    st.stop()

# ---- PROCESS IMAGE & PREDICTION ----
image = Image.open(image_source).resize(IMAGE_SIZE)
image_array = np.asarray(image) / 255.0  # Normalize

# ---- TWO-COLUMN LAYOUT ----
col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown("<h4 style='text-align:center;'>📷 Uploaded/Captured Image</h4>", unsafe_allow_html=True)
    st.image(image_source, width=250, use_column_width=True)
    
    # "Predict" Button (in Left Column)
    if st.button('🔍 Predict'):
        prediction = model.predict(np.expand_dims(image_array, axis=0))
        predicted_class = np.argmax(prediction)
        disease_name = diseases[predicted_class]

        # ---- RIGHT COLUMN: PREDICTION & DISEASE OVERVIEW ----
        with col2:
            st.markdown(f"""
                <div class="info-box">
                    <h3>✅ Prediction: {disease_name}</h3>
                </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""<br>""", unsafe_allow_html=True)

            st.markdown(f"""
                <div class="info-box">
                    <h4>🩺 Disease Overview</h4>
                    <p>{data.loc[predicted_class, 'disease']}</p>
                </div>
            """, unsafe_allow_html=True)

# ---- SUGGESTED TREATMENT (Below Two-Column Layout) ----a

if 'predicted_class' in locals():
        with st.expander("💊 Suggested Treatment"):
            treatment_html = f"""
                <div style="background-color:#1E1E1E; padding:15px; border-radius:10px; color:white;">
                    <h4>📌 Recommended Treatment Plan</h4>
                    <p style="font-size:16px;">{data.loc[predicted_class, 'cure']}</p>
                </div>
            """
            st.markdown(treatment_html, unsafe_allow_html=True)

        # ---- FOOTER (Only After Prediction) ----
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown("""
            <div style="text-align:center; color:#888888; font-size:12px;">
            <p>🔬 Powered by Niramaya AI</p>            
            <p>👩‍💻 Developed by Team Knit Wits</p>
            </div>   
                    
        """, unsafe_allow_html=True)