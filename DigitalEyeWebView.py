import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from DigitalEyeNotification import show_window_notification
from DigitalEyeDetectEye import resource_path
import sys
import DigitalEyeNotificationWorker

icon = resource_path('python.ico')


class WebEnginePage(QWebEnginePage):
    def __init__(self, *args, **kwargs):
        QWebEnginePage.__init__(self, *args, **kwargs)
        self.featurePermissionRequested.connect(self.onFeaturePermissionRequested)
        self.initializeNotificationWorker()
        
    
    def initializeNotificationWorker(self):
       self.obj = DigitalEyeNotificationWorker.DigitalEyeNotificationWorker()  
       self.thread = QThread() 
       self.obj.msgReady.connect(self.onMsgReady)

       self.obj.moveToThread(self.thread)

       self.thread.started.connect(self.obj.procMessage)
       self.thread.start()
       
       
    def onMsgReady(self,message):
        msg = QMessageBox()
        msgHtml = "<p style='text-align: center;'><img src='images/ic_large.png' alt='' width='300' height='180'></p><p style='text-align: center; font-size: 20px;'><strong>"+message+"</strong></p>"
        msg.setIcon(QMessageBox.NoIcon)
        msg.setInformativeText(msgHtml)
        msg.setWindowTitle("Digital Eyes")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setStyleSheet("QLabel{min-width: 700px;}")
        msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        small_icon = QPixmap("images/ic_icon.png")
        msg.setWindowIcon(QIcon(small_icon))
        msg.exec_()
        

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
