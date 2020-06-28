import ctypes
import schedule
from datetime import datetime
import time
from DigitalEyeActions import DigitalEyeActions
from threading import Thread
from DigitalEyeNotificationWorker import DigitalEyeNotificationWorker

class DigitalEyeLockScreen(DigitalEyeActions):
    def __init__(self):
        super().__init__()
        self.run_thread = False
        self.task_thread = None

    def execute_action(self):
        print(datetime.today().__str__(), "Lock Screen Executed")
        DigitalEyeNotificationWorker.message_queue.put("System is going to lock in 1 minute")
        time.sleep(60)
        ctypes.windll.user32.LockWorkStation()
        

    def start_scheduling(self,settings):
        time = settings['lock_system_after']
        if time != '':
            self.run_thread = True
            timeInMinutes = int(time)
            timeInMinutes = timeInMinutes - 1
            schedule.every(timeInMinutes).minutes.do(self.execute_action)
