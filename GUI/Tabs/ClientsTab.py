from http import client

from PySide6 import QtWidgets

from GUI.Widgets.CrudList.CrudList import CrudList
from GUI.Widgets.CrudTable.CrudTable import CrudTable


class ClientsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.list = CrudList("clients")
        self.productTable = CrudTable(["Id", "Name"], "products")
        self.productTable.add_button.setEnabled(False)

        self.list.list.selected.connect(
        self.on_client_selected
    )

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.list)
        layout.addWidget(self.productTable)
    def on_client_selected(self, client):
        client_id = client["id"]

        self.productTable.table.set_client_id(client_id)

        self.productTable.add_button.set_extra_data({
        "client_id": client_id,
    })

        self.productTable.add_button.setEnabled(True)

        self.productTable.table.label.setText(
        f"Books: {client['name']}"
    )