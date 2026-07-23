from PySide6 import QtWidgets, QtCore

import database_controller


class EditClientDialog(QtWidgets.QDialog):
    def __init__(self, client_data, refresh_callback):
        super().__init__()

        self.refresh_callback = refresh_callback
        self.client_data = client_data

        self.setWindowTitle("Edycja klienta")
        self.setFixedSize(400, 300)

        layout = QtWidgets.QFormLayout(self)

        self.name_edit = QtWidgets.QLineEdit()
        self.cut_edit = QtWidgets.QLineEdit()
        self.email_edit = QtWidgets.QLineEdit()

        self.books_list = QtWidgets.QListWidget()

        books = database_controller.load_database("products")

        for book in books:
            item = QtWidgets.QListWidgetItem(book["title"])
            item.setData(QtCore.Qt.ItemDataRole.UserRole, book["id"])
            item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)

            if book["id"] in self.client_data.get("products", []):
                item.setCheckState(QtCore.Qt.CheckState.Checked)
            else:
                item.setCheckState(QtCore.Qt.CheckState.Unchecked)

            self.books_list.addItem(item)

        self.name_edit.setText(str(self.client_data["name"]))
        self.cut_edit.setText(str(self.client_data["cut"]))
        self.email_edit.setText(self.client_data.get("email", ""))


        layout.addRow("Name:", self.name_edit)
        layout.addRow("Cut:", self.cut_edit)
        layout.addRow("Email:", self.email_edit)
        layout.addRow("Books:", self.books_list)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Save |
            QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def save(self):
        self.client_data["name"] = self.name_edit.text()
        self.client_data["cut"] = self.cut_edit.text()
        self.client_data["email"] = self.email_edit.text()

        selected_books = []

        for i in range(self.books_list.count()):
            item = self.books_list.item(i)

            if item.checkState() == QtCore.Qt.CheckState.Checked:
                selected_books.append(item.data(QtCore.Qt.ItemDataRole.UserRole))

        self.client_data["products"] = selected_books

        database = database_controller.load_database("clients")

        for index, client in enumerate(database):
            if client["id"] == self.client_data["id"]:
                database[index] = self.client_data
                break

        database_controller.save_database("clients", database)

        self.refresh_callback()
        self.accept()