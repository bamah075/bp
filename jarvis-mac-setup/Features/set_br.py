import sys
import subprocess


def set_brightness(percentage):
    """
    Set screen brightness (macOS specific)
    percentage: 0-100
    """
    try:
        if sys.platform == "darwin":
            # macOS brightness control using AppleScript
            script = f'''
            tell application "System Events"
                set brightness to {percentage / 100}
            end tell
            '''
            subprocess.run(["osascript", "-e", script], check=False)
            print(f"[Brightness] Set to {percentage}%")

        elif sys.platform == "win32":
            # Windows brightness control (requires wmi)
            try:
                import wmi
                brightness = int(percentage)
                c = wmi.WMI(namespace='wmicore')
                methods = c.WmiMonitorBrightnessMethods()
                if methods:
                    methods[0].WmiSetBrightness(Brightness=brightness)
                    print(f"[Brightness] Set to {percentage}%")
            except Exception as e:
                print(f"[Brightness Error] {e}")

        else:
            print("[Brightness] Not supported on this system")

    except Exception as e:
        print(f"[Brightness Error] {e}")
