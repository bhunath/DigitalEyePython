import ctypes
import schedule
from datetime import datetime
import time


def lock_screen():
    print(datetime.today().__str__(), "Lock Screen Executed")
    ctypes.windll.user32.LockWorkStation()


def start_scheduling(timeInMinute):
    schedule.clear()
    schedule.every(timeInMinute).minutes.do(lock_screen)
    while 1:
        schedule.run_pending()
        time.sleep(1)


def stop_scheduling():
    schedule.clear()
