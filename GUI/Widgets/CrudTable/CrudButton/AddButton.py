from wsgiref.validate import validator

from PySide6 import QtWidgets, QtGui

import database_controller


class AddButton(QtWidgets.QPushButton):
    def __init__(
            self,
            fields: list[str],
            database_name: str,
            refresh_callback,
            suggestions: dict[str, list[str]] = None,
            field_types: dict[str, type] = None
    ):
        super().__init__(f"Add {database_name}")

        self.fields = fields
        self.database_name = database_name
        self.refresh_callback = refresh_callback
        self.suggestions = suggestions or {}
        self.field_types = field_types or {}

        self.clicked.connect(self.add_item_button)

    def create_input(self, field: str):
        options = self.suggestions.get(field.lower())

        if not options:
            line = QtWidgets.QLineEdit()
            line.setPlaceholderText(field.capitalize())

            field_type = self.field_types.get(field.lower())
            if field_type is int:
                line.setValidator(QtGui.QIntValidator())
            elif field_type is float:
                validator = QtGui.QDoubleValidator()
                validator.setDecimals(2)
                line.setValidator(validator)

            return line

        combo = QtWidgets.QComboBox()
        combo.setEditable(True)
        combo.addItems(options)
        combo.setCurrentText("")
        combo.lineEdit().setPlaceholderText(field.capitalize())

        return combo

    def read_input(self, widget):
        if isinstance(widget, QtWidgets.QComboBox):
            return widget.currentText().strip()

        return widget.text()

    def add_item_button(self):
        dialog = QtWidgets.QDialog(self)
        layout = QtWidgets.QVBoxLayout(dialog)

        inputs = {}

        for field in self.fields:
            widget = self.create_input(field)

            layout.addWidget(widget)
            inputs[field.lower()] = widget

        button = QtWidgets.QPushButton("Dodaj")
        layout.addWidget(button)

        button.clicked.connect(dialog.accept)

        if dialog.exec():
            item = {}

            for key, widget in inputs.items():
                item[key] = self.read_input(widget)

            database_controller.item_add(item, self.database_name)
            self.refresh_callback()
