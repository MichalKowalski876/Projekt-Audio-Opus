from PySide6 import QtWidgets
from GUI.Widgets.CrudTable.CrudTable import CrudTable


class ClientsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.clientTable = CrudTable(["Id", "Name", "Cut"], "clients", field_types={"cut":float})
        self.productTable = CrudTable(["Id", "Name"], "products")

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.clientTable)
        layout.addWidget(self.productTable)