import torch
from PIL import Image
from transformers import AutoFeatureExtractor, AutoModelForImageClassification

# Step 1: Load medical vision model (e.g., ViT fine-tuned on Chest X-Rays)
model_name = "nateraw/vit-base-patch16-224-in21k-chestxray"
extractor = AutoFeatureExtractor.from_pretrained(model_name)
model = AutoModelForImageClassification.from_pretrained(model_name)

# Step 2: Load and preprocess image
image = Image.open("chest_xray.jpeg").convert("RGB")
inputs = extractor(images=image, return_tensors="pt")

# Step 3: Run inference to get predictions
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()

finding = model.config.id2label[predicted_class_idx]
print("English Findings:", finding)