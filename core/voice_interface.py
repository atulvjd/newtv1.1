import speech_recognition as sr
from core.speech import speak

recognizer = sr.Recognizer()

def listen_command(timeout=5, phrase_time_limit=10):
    """
    Listen from the microphone and return the recognized command as text.
    :param timeout: Max seconds to wait for speech to start.
    :param phrase_time_limit: Max seconds for the spoken phrase.
    :return: Recognized speech as a string, or None on failure.
    """
    try:
        with sr.Microphone() as source:
            print("🎙️ Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

        print("🔊 Processing...")
        query = recognizer.recognize_google(audio).lower()
        print(f"🔈 You said: {query}")
        return query

    except sr.WaitTimeoutError:
        print("⏱️ No speech detected within timeout.")
        return None
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return None
    except sr.RequestError as e:
        speak("There was an issue with the speech service.")
        print(f"❌ Speech recognition request error: {e}")
        return None
    except Exception as e:
        speak("Unexpected error during voice input.")
        print(f"❌ Voice input error: {e}")
        return None
