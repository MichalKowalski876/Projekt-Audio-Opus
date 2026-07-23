from http import client

from PySide6 import QtWidgets

import database_controller
from GUI.Widgets.CrudList.CrudClientList import CrudClientList
from GUI.Widgets.CrudTable.CrudTable import CrudTable


class ClientsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.list = CrudClientList("clients")

        self.list.list.selected.connect(
        self.on_client_selected
    )

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.list)


    def on_client_selected(self, client):
        client_id = client["id"]

