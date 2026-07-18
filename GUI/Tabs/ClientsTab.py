from http import client

from PySide6 import QtWidgets

import database_controller
from GUI.Widgets.CrudList.CrudClientList import CrudClientList
from GUI.Widgets.CrudTable.CrudTable import CrudTable


class ClientsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.list = CrudClientList("clients")
        self.productTable = CrudTable(["Id", "Name"], "products")

        self.list.list.selected.connect(
        self.on_client_selected
    )

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.list)
        layout.addWidget(self.productTable)

    def show_products(self, product_ids):
        all_products = database_controller.load_database("products")

        self.data = [
            product
            for product in all_products
            if product["id"] in product_ids
        ]

    def on_client_selected(self, client):
        client_id = client["id"]

        self.productTable.table.label.setText(
        f"Books: {client['name']}"
    )

