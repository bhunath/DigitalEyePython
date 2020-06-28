import ctypes
import schedule
from datetime import datetime
import time
from DigitalEyeActions import DigitalEyeActions
from DigitalEyeNotification import show_window_notification
from threading import Thread
from DigitalEyeNotificationWorker import DigitalEyeNotificationWorker

class DigitalEyeBlinkCountNotification(DigitalEyeActions):
    blinks_count = 0
    def __init__(self):
        super().__init__()
        self.run_thread = False
        self.task_thread = None

    def execute_action(self):
        print(datetime.today().__str__(), "Blink Count Executed")
        message = "Avg Blink rate for last 30 Min is "+str(self.blinks_count)
        self.blinks_count = 0
        show_window_notification("Digital Eyes", message)


    def start_scheduling(self,settings):
        time = settings['blink_rate_notification_frequency']
        if time != '':
            timeInInteger = int(time)
            schedule.every(timeInInteger).minutes.do(self.execute_action)