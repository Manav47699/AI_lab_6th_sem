import threading
from io import BytesIO

import torch
from deep_translator import GoogleTranslator
from gtts import gTTS
from PIL import Image
from transformers import AutoFeatureExtractor, AutoModelForImageClassification, logging

import streamlit as st

# Suppress warnings
logging.set_verbosity_error()

# Thread safety lock for model inference
model_lock = threading.Lock()


# Cache model loading for efficiency
@st.cache_resource
def load_medical_model():
    model_name = "nateraw/vit-base-patch16-224-in21k-chestxray"
    extractor = AutoFeatureExtractor.from_pretrained(model_name)
    model = AutoModelForImageClassification.from_pretrained(model_name)
    return extractor, model


extractor, model = load_medical_model()

# App Title & Header
st.title(" Nepali Chest X-Ray Summarizer")
st.write(
    "Upload a Chest X-ray image to get an AI-generated diagnosis, "
    "Nepali translation, and voice summary."
)

# Input: File Uploader or Camera Input
uploaded_file = st.file_uploader(
    "Upload Chest X-Ray Image", type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Chest X-Ray", use_container_width=True)

    with st.spinner("Analyzing Chest X-Ray..."):
        # Stage 1: Vision Model Inference
        with model_lock:
            inputs = extractor(images=image, return_tensors="pt")
            with torch.no_grad():
                outputs = model(**inputs)
                predicted_class_idx = outputs.logits.argmax(-1).item()
                prediction = model.config.id2label[predicted_class_idx]

        # Structure clinical text output
        english_summary = f"Chest X-Ray analysis indicates: {prediction}."

        # Stage 2: Translation to Nepali
        nepali_summary = GoogleTranslator(source="en", target="ne").translate(
            english_summary
        )

        # Stage 3: Text-to-Speech in Nepali
        tts = gTTS(text=nepali_summary, lang="ne")
        mp3_bytes = BytesIO()
        tts.write_to_fp(mp3_bytes)
        mp3_bytes.seek(0)

    # Display Results
    st.markdown("---")
    st.subheader(" Findings & Summary")
    st.write("**English Finding:**", english_summary)
    st.write("**Nepali Summary (नेपाली):**", nepali_summary)

    st.subheader(" Audio Summary (नेपाली आवाज)")
    st.audio(mp3_bytes.read(), format="audio/mp3")