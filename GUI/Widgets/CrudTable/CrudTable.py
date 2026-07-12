from PySide6 import QtWidgets

from GUI.Widgets.CrudTable.CrudButton.AddButton import AddButton
from GUI.Widgets.CrudTable.CrudButton.RemoveButton import RemoveButton
from GUI.Widgets.CrudTable.Table import Table


class CrudTable(QtWidgets.QWidget):
    def __init__(
            self,
            table_header: list[str],
            database_name: str,
            suggestions: dict[str, list[str]] = None
    ):
        super().__init__()

        self.table = Table(table_header, database_name)

        self.add_button = AddButton(
            table_header[1:],          
            database_name,
            self.table.refresh_table,
            suggestions
        )

        self.remove_button = RemoveButton(
            database_name,
            self.table,
            self.table.refresh_table
        )

        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.remove_button)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.addLayout(buttons_layout)
