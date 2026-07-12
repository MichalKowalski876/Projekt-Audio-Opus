import database_controller
import sys
from PySide6.QtWidgets import QApplication

from GUI.WindowPages.MainWindow import MainWindow

if __name__ == '__main__':
    #temp()

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
