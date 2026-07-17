from PySide6 import QtWidgets

from GUI.Widgets.CrudList.CrudList import CrudList
from GUI.Widgets.CrudTable.CrudTable import CrudTable


class ClientsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.list = CrudList("clients")
        self.productTable = CrudTable(["Id", "Name"], "products")

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.list)
        layout.addWidget(self.productTable)