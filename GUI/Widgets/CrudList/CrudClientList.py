from PySide6 import QtWidgets, QtCore

import database_controller
from GUI.Widgets.Buttons.List.EditItemListButton import EditItemListButton
from GUI.Widgets.Buttons.List.AddListButton import AddListButton
from GUI.Widgets.Buttons.List.RemoveListButton import RemoveListButton
from GUI.Widgets.CrudList.List import List
from GUI.Widgets.Dialogs.EditClientDialog import EditClientDialog


class CrudClientList(QtWidgets.QWidget):
    def __init__(self, database_name):
        super().__init__()
        self.current_client = None
        self.list = List(database_name)

        self.details = QtWidgets.QWidget()
        self.details.setFixedWidth(300)

        details_layout = QtWidgets.QFormLayout(self.details)

        self.id_label = QtWidgets.QLabel()
        self.name_label = QtWidgets.QLabel()
        self.cut_label = QtWidgets.QLabel()
        self.email_label = QtWidgets.QLabel()
        self.books_list = QtWidgets.QLabel()

        self.add_button = AddListButton(database_name, self.list.refresh_list)
        self.remove_button = RemoveListButton(database_name, self.list, self.list.refresh_list)
        self.edit_button = EditItemListButton()
        self.edit_button.selected.connect(self.open_edit_window)

        details_layout.addRow("Id:", self.id_label)
        details_layout.addRow("Name:", self.name_label)
        details_layout.addRow("Cut:", self.cut_label)
        details_layout.addRow("Email:", self.email_label)
        details_layout.addRow("Books: ", self.books_list)
        details_layout.addWidget(self.edit_button)

        self.edit_button.hide()

        self.list.selected.connect(self.on_selected_item)

        left_layout = QtWidgets.QVBoxLayout()
        left_layout.addWidget(self.list)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addLayout(left_layout)
        layout.addWidget(self.details)

        layout.setAlignment(
            self.details,
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop
        )

        left_layout.addWidget(self.add_button)
        left_layout.addWidget(self.remove_button)

        layout.setAlignment(
            self.add_button,
            QtCore.Qt.AlignmentFlag.AlignBottom
        )

        layout.setAlignment(
            self.remove_button,
            QtCore.Qt.AlignmentFlag.AlignBottom
        )
    def on_selected_item(self, data):
        self.current_client = data

        self.edit_button.show()

        self.id_label.setText(str(data["id"]))
        self.name_label.setText(data["name"])
        self.cut_label.setText(str(data["cut"]))
        self.email_label.setText(data.get("email", ""))

        books_list_text = ""

        products = database_controller.load_database("products")

        for index, product_id in enumerate(data.get("products", [])):
            product = next(
                (p for p in products if p["id"] == product_id),
                None
            )

            if product is not None:
                books_list_text += f"{index + 1}. {product['name']}\n"

        self.books_list.setText(books_list_text)


    def open_edit_window(self):
        if self.current_client is None:
            return

        dialog = EditClientDialog(self.current_client, self.list.refresh_list)

        if dialog.exec():
            self.on_selected_item(self.current_client)