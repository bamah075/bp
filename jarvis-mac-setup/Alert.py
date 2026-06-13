import sys
import subprocess


def Alert(Text):
    """
    Cross-platform alert system supporting Windows, macOS, and Linux
    """
    try:
        if sys.platform == "win32":
            # Windows: Use winotify for toast notifications
            try:
                from winotify import Notification
                notification = Notification(
                    app_id="JARVIS",
                    title="JARVIS Alert",
                    msg=Text,
                    duration="short"
                )
                notification.show()
            except ImportError:
                print(f"Alert: {Text}")

        elif sys.platform == "darwin":
            # macOS: Use osascript for native notifications
            script = f'''
            display notification "{Text}" with title "JARVIS" subtitle "AI Assistant"
            '''
            subprocess.run(["osascript", "-e", script], check=False)
            print(f"[JARVIS] {Text}")

        else:
            # Linux and other platforms: Console output
            print(f"[JARVIS Alert] {Text}")

    except Exception as e:
        print(f"[JARVIS] {Text}")
        print(f"Alert system error: {e}")
