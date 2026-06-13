import sys
from TextToSpeech.Fast_DF_TTS import speak

def set_brightness_windows(percentage):
    """Cross-platform brightness control"""
    try:
        if sys.platform == "win32":
            import wmi
            w = wmi.WMI(namespace='wmi')
            brightness_methods = w.WmiMonitorBrightnessMethods()[0]
            brightness_methods.WmiSetBrightness(int(percentage), 0)
            speak(f"Brightness set to {percentage}%")
        elif sys.platform == "darwin":
            # macOS brightness control using osascript
            import subprocess
            # Normalize percentage to 0-16 scale for macOS
            mac_brightness = max(0, min(16, int(percentage / 6.25)))
            script = f'tell application "System Events" to key code 144 repeat {mac_brightness}'
            subprocess.run(["osascript", "-e", script], check=False)
            speak(f"Brightness adjusted to approximately {percentage}%")
        else:
            speak("Brightness control not supported on this system")
    except Exception as e:
        speak(f"Error setting brightness: {str(e)}")
