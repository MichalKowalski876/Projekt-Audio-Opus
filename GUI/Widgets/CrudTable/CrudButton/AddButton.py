from PySide6 import QtWidgets

import database_controller


class AddButton(QtWidgets.QPushButton):
    def __init__(self, fields: list[str], database_name: str, refresh_callback):
        super().__init__(f"Add {database_name}")

        self.fields = fields
        self.database_name = database_name
        self.refresh_callback = refresh_callback

        self.clicked.connect(self.add_item_button)

    def add_item_button(self):
        dialog = QtWidgets.QDialog(self)
        layout = QtWidgets.QVBoxLayout(dialog)

        inputs = {}

        for field in self.fields:
            line = QtWidgets.QLineEdit()
            line.setPlaceholderText(field.capitalize())

            layout.addWidget(line)
            inputs[field.lower()] = line

        button = QtWidgets.QPushButton("Dodaj")
        layout.addWidget(button)

        button.clicked.connect(dialog.accept)

        if dialog.exec():
            item = {}

            for key, line in inputs.items():
                item[key] = line.text()

            database_controller.item_add(item, self.database_name)
            self.refresh_callback()