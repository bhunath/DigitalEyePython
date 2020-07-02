from DigitalEyeLongBreak import DigitalEyeLongBreak
from DigitalEyeShortBreak import DigitalEyeShortBreak
from DigitalEyeBlinkCountNotification import DigitalEyeBlinkCountNotification
from DigitalEyeLockScreen import DigitalEyeLockScreen
import time
from threading import Thread
import schedule

class DigitalEyeUtils():
    longBreakObj = DigitalEyeLongBreak()
    shortBreakObj = DigitalEyeShortBreak()
    lockScreenObj = DigitalEyeLockScreen()
    blinkCountObj = DigitalEyeBlinkCountNotification()
    scheduling_thread = None

    def user_settings_updated(self,settings):
        schedule.clear()
        self.longBreakObj.start_scheduling(settings)
        self.shortBreakObj.start_scheduling(settings)
        self.lockScreenObj.start_scheduling(settings)
        self.blinkCountObj.start_scheduling(settings)
        if self.scheduling_thread is None:
            self.scheduling_thread = Thread(target=self.start_scheduler_check)
            self.scheduling_thread.deamon = True
            self.scheduling_thread.start()
                
    def start_scheduler_check(self):
        print("Starting schedule check")
        while True:
            schedule.run_pending()
            time.sleep(1)
        
        
        
        
    def try_long_break(self):
        self.longBreakObj.execute_action()
        return "Success"
    
    def try_blink_notification(self):
        current_blink_count = self.blinkCountObj.blinks_count
        self.blinkCountObj.execute_action()
        self.blinkCountObj.blinks_count = current_blink_count
        return "Success"
    
    
        

    def try_short_break(self):
        self.shortBreakObj.execute_action()
        return "Success"
        