from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtCore import QProcess, QDir, QUrl
from PyQt5.QtWebEngineWidgets import *
import sys


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        q = QDir()
        self.p = QProcess()
        file = q.filePath("SapaTools/SapaTools.exe")
        self.p.setProgram(file)
        self.p.setWorkingDirectory(q.filePath("SapaTools"))
        self.p.start(file, ['runserver', '--noreload'])
        self.p.waitForStarted()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://127.0.0.1:8000/sapa/landing/"))
        self.setCentralWidget(self.browser)
        self.show()


app = QApplication(sys.argv)
window = MainWindow()

app.exec_()
