import sys
import time
import subprocess
import platform
import os

# Pleasant voice options - force natural voices
VOICE_PREFERENCES = {
    'default': 'Samantha',  # Natural female voice
    'alternatives': ['Victoria', 'Moira', 'Karen'],
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
    """Speak text using macOS 'say' command with pleasant natural voice"""
    if not text or len(text.strip()) == 0:
        return

    try:
        if platform.system() == "Darwin":  # macOS
            selected_voice = voice or get_preferred_voice()

            # Force use of Samantha for natural voice (not Alex which is robotic)
            # Samantha is warm and natural, not robotic
            if selected_voice.lower() in ['default', 'alex']:
                selected_voice = 'Samantha'

            # Natural speech parameters
            # -r 130 is very natural, -v sets voice
            subprocess.run([
                "say",
                "-v", selected_voice,      # Use Samantha for warm, natural voice
                "-r", "130",               # Slightly slower for better clarity
                text
            ], check=False)
        else:
            # Fallback to animated text on non-Mac systems
            print_animated_message(text)
    except Exception as e:
        # Fallback if 'say' command fails
        try:
            print_animated_message(text)
        except:
            pass

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

def test_voices():
    """Test all available voices"""
    voices = ['Samantha', 'Victoria', 'Moira', 'Karen', 'Alex']
    for voice in voices:
        try:
            subprocess.run(["say", "-v", voice, f"I am {voice}"], check=False)
            time.sleep(1)
        except:
            pass