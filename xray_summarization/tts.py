from gtts import gTTS

# Nepali summary text
nepali_text = "छातीको एक्स-रेमा तल्लो भागमा न्युमोनियाको लक्षण देखिन्छ।"

# Convert text to speech
tts = gTTS(text=nepali_text, lang="ne")

# Save and play audio file
tts.save("xray_summary_nepali.mp3")
print("Audio saved as xray_summary_nepali.mp3")