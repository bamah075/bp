import os
import sys
from os import getcwd

def Alert(Text):
    """Cross-platform notification system"""
    platform = sys.platform

    try:
        if platform == "win32":
            # Windows: Use winotify
            try:
                from winotify import Notification, audio
                icon_path = r"C:\Users\chatu\OneDrive\Desktop\Jarvis\logo.png"
                toast = Notification(
                    app_id="🟢 J.A.R.V.I.S.",
                    title=Text,
                    duration="long",
                    icon=icon_path if os.path.exists(icon_path) else None
                )
                toast.set_audio(audio.Default, loop=False)
                toast.add_actions(label="Click me", launch="https://www.google.com")
                toast.add_actions(label="Dismiss", launch="https://www.google.com")
                toast.show()
            except ImportError:
                print(f"🟢 J.A.R.V.I.S: {Text}")

        elif platform == "darwin":
            # macOS: Use osascript
            import subprocess
            script = f'display notification "{Text}" with title "J.A.R.V.I.S"'
            subprocess.run(["osascript", "-e", script], check=False)

        else:
            # Linux: Fallback to print
            print(f"🟢 J.A.R.V.I.S: {Text}")

    except Exception as e:
        print(f"🟢 J.A.R.V.I.S: {Text}")
        print(f"Alert Error: {e}")

