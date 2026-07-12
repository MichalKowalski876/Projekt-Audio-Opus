from PySide6 import QtWidgets

from GUI.Widgets.CrudTable.CrudTable import CrudTable


class StreamingTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.crudTable = CrudTable(["Id", "Name", "Price"], "streamings")

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.crudTable)