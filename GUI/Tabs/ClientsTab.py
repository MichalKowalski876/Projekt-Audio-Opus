from PySide6 import QtWidgets, QtCore

import database_controller


class ClientsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.client_id = None
        self.data = None

        self.label = QtWidgets.QLabel("clients", self)
        self.clients_table = QtWidgets.QTableWidget()
        self.clients_table.setFixedSize(315, 400);

        self.clients_table.setColumnCount(3)
        self.clients_table.setHorizontalHeaderLabels([
            "Id",
            "Name",
            "Cut"
        ])

        self.refresh_table()

        self.add_button = QtWidgets.QPushButton("+ Add", self)
        self.add_button.pressed.connect(self.add_client_button)

        self.remove_button = QtWidgets.QPushButton("- Remove", self)
        self.remove_button.pressed.connect(self.remove_client_button)

        self.clients_table.itemChanged.connect(self.on_item_changed)
        self.clients_table.cellClicked.connect(self.on_client_clicked)

        self.setup_layout()

    def add_client_button(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Dodaj klienta")

        layout = QtWidgets.QVBoxLayout(dialog)

        name_input = QtWidgets.QLineEdit()
        name_input.setPlaceholderText("Name")

        cut_input = QtWidgets.QLineEdit()
        cut_input.setPlaceholderText("Cut")

        button = QtWidgets.QPushButton("Dodaj")

        layout.addWidget(name_input)
        layout.addWidget(cut_input)
        layout.addWidget(button)

        button.clicked.connect(dialog.accept)

        if dialog.exec():
            client = {
                "name": name_input.text(),
                "cut": cut_input.text()
            }

            database_controller.item_add(client, "clients")
            self.refresh_table()

    def remove_client_button(self):
        id, ok = QtWidgets.QInputDialog.getText(
            self,
            "Usuń klienta",
            "Podaj id:"
        )

        if ok:
            database_controller.item_remove(int(id), "clients")
            self.refresh_table()

    def on_item_changed(self, item):
        column_id = self.clients_table.item(item.row(),0)
        field = self.clients_table.horizontalHeaderItem(item.column())

        database_controller.item_modify(
            int(column_id.text()),
            field.text().lower(),
            item.text(),
            "clients"
        )

    def on_client_clicked(self, row):
        self.client_id = self.clients_table.item(row, 0).text()

    def refresh_table(self):
        self.data = database_controller.load_database()

        self.clients_table.setRowCount(len(self.data))

        for row, client in enumerate(self.data):
            self.clients_table.setItem(
                row, 0,
                QtWidgets.QTableWidgetItem(str(client["id"]))
            )
            self.clients_table.setItem(
                row, 1,
                QtWidgets.QTableWidgetItem(client["name"])
            )
            self.clients_table.setItem(
                row, 2,
                QtWidgets.QTableWidgetItem(client["cut"])
            )

    def setup_layout(self):
        layout = QtWidgets.QVBoxLayout(self)

        layout.addWidget(
            self.label,
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            self.clients_table,
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.add_button,
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        layout.addWidget(
            self.remove_button,
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)