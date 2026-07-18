from wsgiref.validate import validator

from PySide6 import QtWidgets, QtGui

import database_controller


class AddListButton(QtWidgets.QPushButton):
    def __init__(
            self,
            database_name: str,
            refresh_callback
    ):
        super().__init__(f"Add {database_name}")

        self.database_name = database_name
        self.refresh_callback = refresh_callback

        self.clicked.connect(self.add_button_logic)

    def add_button_logic(self):
        new_client = {
            "name": "new client",
            "cut" : 0,
            "email": None
        }
        database_controller.item_add( new_client, self.database_name)

        self.refresh_callback()