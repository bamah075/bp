import sys
import time
import subprocess
import platform

def print_animated_message(message):
    """Print text with animation effect in terminal"""
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.025)
    print()

def speak(text):
    """Speak text using macOS 'say' command or fallback to animated text"""
    try:
        if platform.system() == "Darwin":  # macOS
            # Use macOS built-in 'say' command for voice output
            subprocess.run(["say", text], check=True)
        else:
            # Fallback to animated text on non-Mac systems
            print_animated_message(text)
    except Exception:
        # Fallback if 'say' command fails
        print_animated_message(text)