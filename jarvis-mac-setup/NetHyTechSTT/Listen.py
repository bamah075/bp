import sys

try:
    import speech_recognition as sr
except ImportError:
    sr = None


class Listener:
    """
    Cross-platform speech recognition using SpeechRecognition
    """

    def __init__(self):
        if sr is None:
            print("[Warning] speech_recognition not installed. Install with: pip install SpeechRecognition")
        self.recognizer = sr.Recognizer() if sr else None

    def listen(self):
        """
        Listen for voice input and return recognized text
        """
        if not self.recognizer or not sr:
            print("[Listener] Speech recognition unavailable")
            return None

        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.1)
                print("[Listening...]")
                audio = self.recognizer.listen(source, timeout=5)

            # Try Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            return text

        except sr.UnknownValueError:
            print("[Listener] Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"[Listener Error] {e}")
            return None
        except Exception as e:
            print(f"[Listener Error] {e}")
            return None
