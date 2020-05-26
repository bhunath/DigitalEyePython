import threading
from DigitalEyeServer import start_server


class ServerThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        start_server()
