import ctypes
import schedule
from datetime import datetime
import time
from DigitalEyeActions import DigitalEyeActions
from DigitalEyeNotification import show_window_notification
from threading import Thread
from DigitalEyeNotificationWorker import DigitalEyeNotificationWorker

class DigitalEyeShortBreak(DigitalEyeActions):
    def __init__(self):
        super().__init__()
        self.run_thread = False
        self.task_thread = None

    def execute_action(self):
        print(datetime.today().__str__(), "Short break Executed")
        message = "Time For a short break!"
        show_window_notification("Digital Eyes", message)
        DigitalEyeNotificationWorker.message_queue.put(message)
        

    def start_scheduling(self,settings):
        time = settings['short_break_every']
        if time != '':
            self.run_thread = True
            timeInInteger = int(time)
            schedule.every(timeInInteger).minutes.do(self.execute_action)
            