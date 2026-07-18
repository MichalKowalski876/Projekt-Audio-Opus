from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QHeaderView

from GUI.Widgets.CrudTable.NumericDelegate import NumericDelegate
import database_controller


class Table(QtWidgets.QWidget):
    def __init__(self, table_header: list[str], database_name: str):
        super().__init__()

        self.table_header = table_header
        self.database_name = database_name

        self.data = []
        self.item_id = None

        self.label = QtWidgets.QLabel(database_name.capitalize())

        self.table = QtWidgets.QTableWidget()
        self.table.setFixedSize(315, 400)

        self.table.setColumnCount(len(self.table_header))
        self.table.setHorizontalHeaderLabels(self.table_header)

        if "Cut" in self.table_header:
            column = self.table_header.index("Cut")
            self.table.setItemDelegateForColumn(
                column,
                NumericDelegate(float, self.table)
            )

        if self.database_name == "products":
            header = self.table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.Stretch)

        self.table.itemChanged.connect(self.on_item_changed)
        self.table.cellClicked.connect(self.on_item_clicked)

        self.setup_layout()
        self.refresh_table()

    def on_item_changed(self, item):
        column_id = self.table.item(item.row(), 0)
        field = self.table.horizontalHeaderItem(item.column())

        database_controller.item_modify(
            int(column_id.text()),
            field.text().lower(),
            item.text(),
            self.database_name
        )

    def on_item_clicked(self, row, column):
        self.item_id = int(self.table.item(row, 0).text())

    def refresh_table(self):
        self.data = database_controller.load_database(self.database_name)

        self.table.blockSignals(True)
        self.table.setRowCount(len(self.data))

        for row, item in enumerate(self.data):
            for column, header in enumerate(self.table_header):
                value = item.get(header.lower(), "")
                self.table.setItem(
                    row,
                    column,
                    QtWidgets.QTableWidgetItem(str(value))
                )

        self.table.blockSignals(False)

    def setup_layout(self):
        layout = QtWidgets.QVBoxLayout(self)

        layout.addWidget(
            self.label,
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.table,
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)