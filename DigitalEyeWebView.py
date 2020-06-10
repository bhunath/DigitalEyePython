import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from DigitalEyeNotification import show_window_notification
from DigitalEyeDetectEye import resource_path

icon = resource_path('python.ico')


class WebEnginePage(QWebEnginePage):
    def __init__(self, *args, **kwargs):
        QWebEnginePage.__init__(self, *args, **kwargs)
        self.featurePermissionRequested.connect(self.onFeaturePermissionRequested)

    def onFeaturePermissionRequested(self, url, feature):
        if feature in (QWebEnginePage.MediaAudioCapture,
                       QWebEnginePage.MediaVideoCapture,
                       QWebEnginePage.MediaAudioVideoCapture):
            self.setFeaturePermission(url, feature, QWebEnginePage.PermissionGrantedByUser)
        else:
            self.setFeaturePermission(url, feature, QWebEnginePage.PermissionDeniedByUser)

    def javaScriptConsoleMessage(self, QWebEnginePage_JavaScriptConsoleMessageLevel, p_str, p_int, p_str_1):
        print('Console Call', QWebEnginePage_JavaScriptConsoleMessageLevel, p_str, p_int, p_str_1)
        if p_str is not None and "Notification" in p_str:
            show_window_notification('Console Call', p_str,icon)


def start_web_view():
    app = QApplication(sys.argv)
    # window = MainWindow()
    # window.show()
    view = QWebEngineView()
    page = WebEnginePage()
    view.setPage(page)
    view.setWindowTitle("Digital Eyes")
    view.load(QUrl("https://bhunath.github.io/DigitalEyesReporting/DigitalEyes.html"))
    view.show()
    sys.exit(app.exec_())
