from PySide6 import QtWidgets

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

        self.name_edit.setText(str(self.client_data["name"]))
        self.cut_edit.setText(str(self.client_data["cut"]))
        self.email_edit.setText(self.client_data.get("email", ""))

        layout.addRow("Name:", self.name_edit)
        layout.addRow("Cut:", self.cut_edit)
        layout.addRow("Email:", self.email_edit)

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

        database = database_controller.load_database("clients")

        for index, client in enumerate(database):
            if client["id"] == self.client_data["id"]:
                database[index] = self.client_data
                break

        database_controller.save_database("clients", database)

        self.refresh_callback()

        self.accept()