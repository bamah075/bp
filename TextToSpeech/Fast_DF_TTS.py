import sys
import time
import subprocess
import platform
import os

try:
    import pyttsx3
    HAS_PYTTSX3 = True
except ImportError:
    HAS_PYTTSX3 = False

# Initialize pyttsx3 engine with better voice
if HAS_PYTTSX3:
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 135)  # Natural speech rate
        engine.setProperty('volume', 0.9)  # Good volume

        # Try to set a natural female voice
        voices = engine.getProperty('voices')
        if len(voices) > 1:
            # Usually voices[1] is female, voices[0] is male
            engine.setProperty('voice', voices[1].id)
    except Exception:
        engine = None
else:
    engine = None

def print_animated_message(message):
    """Print text with animation effect in terminal"""
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.025)
    print()

def get_preferred_voice():
    """Get the preferred voice"""
    return os.getenv('MAYA_VOICE', 'default')

def speak(text, voice=None):
    """Speak text using best available TTS"""
    if not text or len(text.strip()) == 0:
        return

    try:
        if platform.system() == "Darwin":  # macOS with say command
            try:
                selected_voice = voice or get_preferred_voice()
                if selected_voice.lower() in ['default', 'alex']:
                    selected_voice = 'Samantha'

                subprocess.run([
                    "say",
                    "-v", selected_voice,
                    "-r", "130",
                    text
                ], check=False, timeout=30)
                return
            except Exception:
                pass

        # Use pyttsx3 for Linux/Windows or macOS fallback
        if HAS_PYTTSX3 and engine:
            try:
                engine.say(text)
                engine.runAndWait()
                return
            except Exception:
                pass

        # Final fallback: print to terminal
        print_animated_message(text)

    except Exception:
        try:
            print_animated_message(text)
        except:
            pass

def get_available_voices():
    """Get list of available voices"""
    if HAS_PYTTSX3:
        try:
            engine_temp = pyttsx3.init()
            voices = engine_temp.getProperty('voices')
            return [v.name for v in voices]
        except Exception:
            return []
    elif platform.system() == "Darwin":
        try:
            result = subprocess.run(["say", "-v", "?"], capture_output=True, text=True)
            return result.stdout.split('\n')
        except Exception:
            return []
    return []

def set_voice(voice_name):
    """Set the voice for Maya"""
    global engine
    os.environ['MAYA_VOICE'] = voice_name

    if HAS_PYTTSX3 and engine:
        try:
            voices = engine.getProperty('voices')
            for voice in voices:
                if voice_name.lower() in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    return
        except Exception:
            pass

def test_voice():
    """Test current voice"""
    speak("Hello! I am Maya. How can I help you today?")