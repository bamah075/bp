import os


def check_schedule(file_path):
    """
    Check and process scheduled tasks from schedule.txt
    """
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                schedules = f.readlines()
            print(f"[Schedule] Found {len(schedules)} scheduled tasks")
        else:
            print("[Schedule] No schedule file found")
    except Exception as e:
        print(f"[Schedule Error] {e}")


def check_Alam(file_path):
    """
    Check and process alarms from Alam_data.txt
    """
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                alarms = f.readlines()
            print(f"[Alarms] Found {len(alarms)} alarm(s)")
        else:
            print("[Alarms] No alarms file found")
    except Exception as e:
        print(f"[Alarms Error] {e}")
