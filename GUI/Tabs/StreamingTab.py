from PySide6 import QtWidgets, QtCore

import database_controller


class StreamingTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()



        self.setupLayout()

    def setupLayout(self):
        self.setLayout(QtWidgets.QVBoxLayout())

