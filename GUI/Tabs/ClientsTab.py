from PySide6 import QtWidgets
from GUI.Widgets.CrudTable.CrudTable import CrudTable


class ClientsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.crudTable = CrudTable(["Id", "Name", "Cut"], "clients")

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.crudTable)