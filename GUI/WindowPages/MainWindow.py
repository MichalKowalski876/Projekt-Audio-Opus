from PySide6 import QtWidgets, QtCore
from PySide6 import QtWidgets

from GUI.Tabs.ClientsTab import ClientsTab
from GUI.Tabs.StreamingTab import StreamingTab
from GUI.Tabs.ReportTab import ReportTab

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Projekt Audio Opus")
        self.resize(1000, 700)

        self.tabs = QtWidgets.QTabWidget()

        self.tabs.addTab(ClientsTab(), "Clients")
        self.tabs.addTab(StreamingTab(), "Streaming")
        self.tabs.addTab(ReportTab(), "Report on E-mail")

        self.setCentralWidget(self.tabs)
