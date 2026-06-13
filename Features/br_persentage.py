import sys
from TextToSpeech.Fast_DF_TTS import speak

def get_brightness_windows():
    """Cross-platform brightness getter"""
    try:
        if sys.platform == "win32":
            import wmi
            w = wmi.WMI(namespace='wmi')
            brightness_methods = w.WmiMonitorBrightness()
            brightness_percentage = brightness_methods[0].CurrentBrightness
            return brightness_percentage
        elif sys.platform == "darwin":
            # macOS: Use ioreg to get brightness
            import subprocess
            result = subprocess.run(
                ["ioreg", "-r", "-k", "IODisplayBrightness"],
                capture_output=True, text=True
            )
            if "IODisplayBrightness" in result.stdout:
                return "Unknown (macOS)"
            return 50  # Default estimate
        else:
            return "Unavailable"
    except Exception as e:
        return f"Error: {e}"

def check_br_persentage():
    brightness = get_brightness_windows()
    speak(f"Current Brightness: {brightness}%")

