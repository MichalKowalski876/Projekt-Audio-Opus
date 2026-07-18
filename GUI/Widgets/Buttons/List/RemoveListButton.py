from PySide6 import QtWidgets

import database_controller


class RemoveListButton(QtWidgets.QPushButton):
    def __init__(self, database_name: str, list, refresh_callback):
        super().__init__("Remove")

        self.database_name = database_name
        self.list = list
        self.refresh_callback = refresh_callback

        self.clicked.connect(self.remove_item)

    def remove_item(self):
        if self.list.item_id is None:
            QtWidgets.QMessageBox.warning(
                self,
                "Warning",
                "Select a item first."
            )
            return

        database_controller.item_remove(
            self.list.item_id,
            self.database_name
        )

        self.list.item_id = None
        self.refresh_callback()