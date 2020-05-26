import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from DigitalEyeServerThread import ServerThread
import _thread


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Digital Eyes")
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://bhunath.github.io/DigitalEyesReporting/DigitalEyes.html"))
        self.setCentralWidget(self.browser)


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


