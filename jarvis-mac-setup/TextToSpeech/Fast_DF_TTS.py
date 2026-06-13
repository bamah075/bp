import sys
import pyttsx3


def speak(text):
    """
    Cross-platform text-to-speech using pyttsx3
    Works on Windows, macOS, and Linux
    """
    try:
        engine = pyttsx3.init()

        if sys.platform == "darwin":
            # macOS specific voice settings
            voices = engine.getProperty('voices')
            if voices:
                engine.setProperty('voice', voices[0].id)
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)

        elif sys.platform == "win32":
            # Windows voice settings
            engine.setProperty('rate', 150)

        else:
            # Linux voice settings
            engine.setProperty('rate', 150)

        engine.say(text)
        engine.runAndWait()
        engine.stop()

    except Exception as e:
        print(f"[TTS Error] {e}")
