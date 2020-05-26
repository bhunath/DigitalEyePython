from DigitalEyeServerThread import ServerThread
from DigitalEyeUIThread import UIThread


def start_application():
    server_thread = ServerThread()
    ui_thread = UIThread()

    server_thread.start()
    ui_thread.start()


if __name__ == '__main__':
    start_application()
