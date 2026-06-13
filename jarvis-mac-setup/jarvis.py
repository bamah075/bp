import threading
import os
from internet_check import is_Online
from Alert import Alert
from Data.DLG_Data import online_dlg, offline_dlg
import random
from co_brain import Jarvis
from TextToSpeech.Fast_DF_TTS import speak
from Automation.Battery import check_plug
from Time_Operations.throw_alert import check_schedule, check_Alam
from os import getcwd

# Cross-platform path handling
Alam_path = os.path.join(getcwd(), "Alam_data.txt")
file_path = os.path.join(getcwd(), "schedule.txt")

ran_online_dlg = random.choice(online_dlg)
ran_offline_dlg = random.choice(offline_dlg)


def main():
    try:
        online = is_Online()
    except Exception:
        online = False

    if online:
        status_msg = ran_online_dlg
    else:
        status_msg = ran_offline_dlg

    t1 = threading.Thread(target=speak, args=(status_msg,))
    t3 = threading.Thread(target=check_plug)
    t4 = threading.Thread(target=check_schedule, args=(file_path,))
    t5 = threading.Thread(target=Jarvis)
    t6 = threading.Thread(target=check_Alam, args=(Alam_path,))

    t1.start()
    t1.join()

    t3.start()
    t4.start()
    t5.start()
    t6.start()

    t3.join()
    t4.join()
    t5.join()
    t6.join()


if __name__ == "__main__":
    main()
