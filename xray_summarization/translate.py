from deep_translator import GoogleTranslator

# English clinical finding from vision stage
english_findings = "The chest X-ray shows signs consistent with Pneumonia in the lower lobe."

# Translate English summary to Nepali
nepali_summary = GoogleTranslator(source="en", target="ne").translate(english_findings)

print("Nepali Summary:", nepali_summary)