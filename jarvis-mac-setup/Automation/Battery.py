import subprocess
import sys


def check_plug():
    """
    Check if device is plugged in and battery status
    """
    try:
        if sys.platform == "darwin":
            # macOS battery check
            result = subprocess.run(
                ["pmset", "-g", "batt"],
                capture_output=True,
                text=True
            )
            print(f"[Battery Status] {result.stdout}")

        elif sys.platform == "win32":
            # Windows battery check
            result = subprocess.run(
                ["wmic", "path", "win32_battery", "get", "estimatedchargeremaining"],
                capture_output=True,
                text=True
            )
            print(f"[Battery Status] {result.stdout}")

        else:
            # Linux battery check
            result = subprocess.run(
                ["acpi", "-b"],
                capture_output=True,
                text=True
            )
            if result.stdout:
                print(f"[Battery Status] {result.stdout}")
            else:
                print("[Battery] Status unavailable on this system")

    except Exception as e:
        print(f"[Battery Check Error] {e}")
