from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox)
from PyQt5.QtCore import QProcess, QDir, QUrl
from PyQt5.QtWebEngineWidgets import *
import sys
import psutil


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.p = QProcess()
        self.browser = QWebEngineView()

        if self.process_is_running("SAGE.exe") < 3:
            self.run_app()
        else:
            sys.exit()

    def run_app(self):
        q = QDir()
        file = q.filePath("SageTools/SageTools.exe")
        self.p.setProgram(file)
        self.p.setWorkingDirectory(q.filePath("SageTools"))
        self.p.start(file, ['runserver', '--noreload'])
        self.p.waitForStarted()

        self.browser.setUrl(QUrl("http://127.0.0.1:8000/sage/landing/"))
        self.setCentralWidget(self.browser)
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
