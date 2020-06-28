import ctypes
import schedule
from datetime import datetime
import time
from DigitalEyeActions import DigitalEyeActions
from DigitalEyeNotification import show_window_notification
from threading import Thread
from DigitalEyeNotificationWorker import DigitalEyeNotificationWorker

class DigitalEyeLongBreak(DigitalEyeActions):
    def __init__(self):
        super().__init__()
        self.run_thread = False
        self.task_thread = None

    def execute_action(self):
        print(datetime.today().__str__(), "Long break Executed")
        message = "Its time for a long break. Spend a few minutes taking rest from the display."
        show_window_notification("Digital Eyes", message)
        DigitalEyeNotificationWorker.message_queue.put(message)


    def start_scheduling(self,settings):
        time = settings['long_break_every']
        timeBefore = settings['long_break_notify']
        if time != '':
            self.run_thread = True
            timeInInteger = int(time)
            if timeBefore != '':
                timeInInteger = timeInInteger - int(timeBefore)
            schedule.every(timeInInteger).minutes.do(self.execute_action)