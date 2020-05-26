import threading
from DigitalEyeWebView import start_web_view


class UIThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        start_web_view()
