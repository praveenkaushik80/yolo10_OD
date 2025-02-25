import streamlit as st
import cv2
import numpy as np
import PIL
from pathlib import Path

# Local Modules
import settings
import helper
from helper import _display_detected_frames  # Ensure this import
import warnings
warnings.filterwarnings("ignore")
# Setting page layout
st.set_page_config(
    page_title="Object Detection",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Insert the logo at the top of the app
st.image("mcg_brandlogo.webp", width=100)  # Adjust the width as needed
# Main page heading
st.title("Object Detection")

# Sidebar
st.sidebar.header("ML Model Config")

# Model Options
confidence = float(st.sidebar.slider("Select Model Confidence", 15, 100, 20)) / 100

# Load Pre-trained ML Model
model_path = Path(settings.DETECTION_MODEL)
try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

st.sidebar.header("Image/Video Config")
source_radio = st.sidebar.radio("Select Source", settings.SOURCES_LIST)
source_img = None

# If image is selected
if source_radio == settings.IMAGE:
    source_img = st.sidebar.file_uploader("Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))
    col1, col2 = st.columns(2)
    with col1:
        try:
            if source_img is None:
                default_image_path = str(settings.DEFAULT_IMAGE)
                default_image = PIL.Image.open(default_image_path)
                st.image(default_image_path, caption="Default Image", use_container_width=True)
            else:
                uploaded_image = PIL.Image.open(source_img)
                st.image(source_img, caption="Uploaded Image", use_container_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)
    with col2:
        if source_img is None:
            default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
            default_detected_image = PIL.Image.open(default_detected_image_path)
            st.image(default_detected_image_path, caption='Detected Image', use_container_width=True)
        else:
            if st.sidebar.button('Detect Objects'):
                try:
                    # Convert PIL image to OpenCV format
                    image_np = np.array(uploaded_image)
                    _display_detected_frames(confidence, model, st, image_np)
                except Exception as ex:
                    st.error("Error occurred while detecting objects.")
                    st.error(ex)

# If video is selected
elif source_radio == settings.VIDEO:
    helper.play_stored_video(confidence, model)
