from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox)
from PyQt5.QtCore import QProcess, QDir, QUrl
from PyQt5 import QtGui
from PyQt5.QtWebEngineWidgets import *
import sys
import psutil


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.p = QProcess()
        self.browser = QWebEngineView()

        if self.process_is_running("SAPA.exe") < 3:
            self.run_app()
        else:
            sys.exit()

    def run_app(self):
        q = QDir()
        file = q.filePath("SapaTools/SapaTools.exe")
        self.p.setProgram(file)
        self.p.setWorkingDirectory(q.filePath("SapaTools"))
        self.p.start(file, ['runserver', '--noreload'])
        self.p.waitForStarted()

        self.browser.setWindowIcon(QtGui.QIcon('SAPA.ico'))
        self.browser.setUrl(QUrl("http://127.0.0.1:8000/sapa/landing/"))
        self.setCentralWidget(self.browser)
        self.show()
        self.showMaximized()

    def process_is_running(self, process_name):
        processes_running = 0
        for process in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if process_name.lower() in process.name().lower():
                    processes_running += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return processes_running

    def closeEvent(self, event):
        result = QMessageBox.question(self,
                                      "Confirm Exit Application",
                                      "Are you sure you want to exit the app ?",
                                      QMessageBox.Yes | QMessageBox.No)

        if result == QMessageBox.No:
            event.ignore()


app = QApplication(sys.argv)
window = MainWindow()
app.exec_()
