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
    timeInInteger = 0
    def __init__(self):
        super().__init__()
        self.run_thread = False
        self.task_thread = None

    def execute_action(self):
        print(datetime.today().__str__(), "Blink Count Executed")
        blink_average = self.blinks_count
        if blink_average > 0 :
            blink_average = blink_average/self.timeInInteger
        message = "Avg Blink rate for last "+str(self.timeInInteger)+" Min is "+str(blink_average)
        self.blinks_count = 0
        show_window_notification("Digital Eyes", message)


    def start_scheduling(self,settings):
        time = settings['blink_rate_notification_frequency']
        if time != '':
            self.timeInInteger = int(time)
            schedule.every(self.timeInInteger).minutes.do(self.execute_action)