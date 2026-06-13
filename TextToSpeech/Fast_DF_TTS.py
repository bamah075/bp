import sys
import time
import subprocess
import platform
import os

# Pleasant voice options
VOICE_PREFERENCES = {
    'default': 'Samantha',  # Natural female voice
    'alternatives': ['Victoria', 'Moira', 'Karen'],  # Other pleasant voices
}

def print_animated_message(message):
    """Print text with animation effect in terminal"""
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.025)
    print()

def get_preferred_voice():
    """Get the preferred voice from environment or use default"""
    env_voice = os.getenv('MAYA_VOICE')
    if env_voice:
        return env_voice
    return VOICE_PREFERENCES['default']

def speak(text, voice=None):
    """Speak text using macOS 'say' command with pleasant voice"""
    try:
        if platform.system() == "Darwin":  # macOS
            selected_voice = voice or get_preferred_voice()
            # Use macOS built-in 'say' command with selected voice
            # -r controls speech rate (default 200 wpm), use 150 for natural sounding
            subprocess.run([
                "say",
                "-v", selected_voice,
                "-r", "150",  # Natural speech rate
                text
            ], check=True)
        else:
            # Fallback to animated text on non-Mac systems
            print_animated_message(text)
    except Exception as e:
        # Fallback if 'say' command fails
        print_animated_message(text)

def get_available_voices():
    """Get list of available macOS voices"""
    try:
        if platform.system() == "Darwin":
            result = subprocess.run(["say", "-v", "?"], capture_output=True, text=True)
            return result.stdout.split('\n')
        return []
    except Exception:
        return VOICE_PREFERENCES['alternatives']

def set_voice(voice_name):
    """Set the voice for Maya"""
    os.environ['MAYA_VOICE'] = voice_name