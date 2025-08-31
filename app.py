import pickle
import numpy as np
import streamlit as st
import base64
from PIL import Image

# Page config to remove header
st.set_page_config(
    page_title="Crop Yield Predictor",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit header and menu
st.markdown("""
<style>
    .reportview-container {
        margin-top: -2em;
    }
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    #stDecoration {display:none;}
    header {visibility: hidden;}
    
    .main {
        background-image: url("data:image/jpeg;base64,{}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    .stApp > div:first-child {
        background-image: url("data:image/jpeg;base64,{}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
</style>
""", unsafe_allow_html=True)

# Function to encode image to base64
@st.cache_data
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

# Load background image
img_base64 = get_base64_image("getty-images-r_rXoOYAvy4-unsplash-1024x681.jpg")

# Apply background image
if img_base64:
    st.markdown(f"""
    <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
    </style>
    """, unsafe_allow_html=True)

# Load the trained model
@st.cache_resource
def load_model():
    try:
        with open('trained_model.sav', 'rb') as file:
            return pickle.load(file)
    except:
        return None

model = load_model()

# Main app
st.markdown('<div class="input-container">', unsafe_allow_html=True)
st.title("🌾 Crop Yield Predictor")
st.markdown('</div>', unsafe_allow_html=True)

if model is None:
    st.error("Model file not found. Please ensure 'trained_model.sav' exists in the directory.")
else:
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        area = st.number_input("Area (hectares)", min_value=0.0, value=100.0, step=1.0)
        item = st.selectbox("Crop Type", ["Wheat", "Rice", "Maize", "Barley", "Soybeans", "Other"])
        year = st.number_input("Year", min_value=1990, max_value=2030, value=2023, step=1)
    
    with col2:
        rainfall = st.number_input("Average Rainfall (mm/year)", min_value=0.0, value=500.0, step=10.0)
        pesticides = st.number_input("Pesticides (tonnes)", min_value=0.0, value=10.0, step=0.1)
        avg_temp = st.number_input("Average Temperature (°C)", min_value=-10.0, max_value=50.0, value=25.0, step=0.1)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Predict Crop Yield", type="primary"):
        # Encode categorical variable (Item)
        item_encoded = hash(item) % 1000  # Simple encoding for demo
        
        # Prepare input features
        features = np.array([[area, item_encoded, year, rainfall, pesticides, avg_temp]])
        
        try:
            # Make prediction
            prediction = model.predict(features)[0]
            
            st.markdown('<div class="prediction-container">', unsafe_allow_html=True)
            st.success(f"🎯 Predicted Crop Yield: **{prediction:.2f} tonnes**")
            
            # Additional insights
            st.info(f"""
            **Prediction Summary:**
            - Crop: {item}
            - Area: {area} hectares
            - Expected yield per hectare: {prediction/area:.2f} tonnes/hectare
            """)
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error making prediction: {str(e)}")
            st.info("Please ensure the model was trained with compatible features.")

# Footer
st.markdown('<div class="input-container">', unsafe_allow_html=True)
st.markdown("---")
st.markdown("*Crop Yield Prediction using Machine Learning*")
st.markdown('</div>', unsafe_allow_html=True)