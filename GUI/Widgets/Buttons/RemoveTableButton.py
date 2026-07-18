from PySide6 import QtWidgets

import database_controller


class RemoveTableButton(QtWidgets.QPushButton):
    def __init__(self, database_name: str, table, refresh_callback):
        super().__init__("Remove")

        self.database_name = database_name
        self.table = table
        self.refresh_callback = refresh_callback

        self.clicked.connect(self.remove_item)

    def remove_item(self):
        if self.table.item_id is None:
            QtWidgets.QMessageBox.warning(
                self,
                "Warning",
                "Select a row first."
            )
            return

        database_controller.item_remove(
            self.table.item_id,
            self.database_name
        )

        self.table.item_id = None
        self.refresh_callback()