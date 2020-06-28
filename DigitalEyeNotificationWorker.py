from PyQt5.QtCore import (QObject, pyqtSignal, pyqtSlot)
from queue import Queue
import time

class DigitalEyeNotificationWorker(QObject):
    msgReady = pyqtSignal(str)
    message_queue = Queue()
    
    @pyqtSlot()
    def procMessage(self):
        print("Procuring Messages")
        while True:
            time.sleep(1)
            msg = self.message_queue.get()
            if msg != '':
                self.msgReady.emit(msg)
            
            
    