import os
import streamlit as st
import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification

# Set page config
st.set_page_config(
    page_title="Nepali Chest X-Ray Summarizer",
    page_icon="🩺",
    layout="centered"
)

@st.cache_resource
def load_medical_model():
    # Verified public Hugging Face model
    model_name = "google/vit-base-patch16-224"
    
    # Optional HF Token if working with private/gated models
    hf_token = os.getenv("HF_TOKEN", None)
    
    processor = AutoImageProcessor.from_pretrained(
        model_name, 
        token=hf_token
    )
    model = AutoModelForImageClassification.from_pretrained(
        model_name, 
        token=hf_token
    )
    return processor, model

# Load model and processor
processor, model = load_medical_model()

# App Title & Header
st.title("🩺 Nepali Chest X-Ray Summarizer")
st.write("Upload a chest X-ray image to get an automated classification summary.")

# File Uploader
uploaded_file = st.file_uploader("Choose an X-Ray Image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded X-Ray", use_column_width=True)

    if st.button("Analyze X-Ray"):
        with st.spinner("Analyzing image..."):
            # Preprocess image and perform inference
            inputs = processor(images=image, return_tensors="pt")
            
            with torch.no_grad():
                outputs = model(**inputs)
                logits = outputs.logits
                predicted_class_id = logits.argmax(-1).item()
                confidence = torch.softmax(logits, dim=-1)[0][predicted_class_id].item()

            label = model.config.id2label[predicted_class_id]

            # Display results
            st.success("Analysis Complete!")
            st.metric(label="Predicted Finding", value=label.capitalize())
            st.write(f"**Confidence Score:** {confidence * 100:.2f}%")