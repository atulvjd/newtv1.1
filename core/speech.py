import pyttsx3
import platform

# Initialize text-to-speech engine
engine = pyttsx3.init()

# === CONFIGURATION ===
engine.setProperty("rate", 180)  # Speaking rate (words per minute)
engine.setProperty("volume", 1.0)  # Max volume

# Set default voice based on OS
voices = engine.getProperty("voices")
if platform.system() == "Windows":
    # Prefer Zira (female) voice if available
    for voice in voices:
        if "zira" in voice.name.lower():
            engine.setProperty("voice", voice.id)
            break
    else:
        engine.setProperty("voice", voices[0].id)
else:
    # macOS/Linux: use first available voice
    engine.setProperty("voice", voices[0].id)

# === SPEAK FUNCTION ===
def speak(text: str):
    """Speak the given text using TTS engine."""
    try:
        print(f"🗣️ Speaking: {text}")
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"❌ Speech error: {e}")
        print(f"(Fallback) {text}")
