from PySide6 import QtWidgets, QtCore
import database_controller


class List(QtWidgets.QWidget):
    selected = QtCore.Signal(dict)
    def __init__(self, database_name: str):
        super().__init__()

        self.database_name = database_name
        self.data = []
        self.item_id = None

        self.label = QtWidgets.QLabel(database_name.capitalize())

        self.list = QtWidgets.QListWidget()
        self.list.setFixedSize(120, 400)

        self.refresh_list()

        self.list.itemClicked.connect(self.on_item_clicked)

        self.setup_layout()

    def refresh_list(self):
        self.data = database_controller.load_database(self.database_name)

        self.list.clear()

        for item in self.data:
            list_item = QtWidgets.QListWidgetItem(item["name"])
            list_item.setData(QtCore.Qt.ItemDataRole.UserRole, item)
            self.list.addItem(list_item)

    def on_item_clicked(self, item):
        data = item.data(QtCore.Qt.ItemDataRole.UserRole)

        self.item_id = data["id"]
        self.selected.emit(data)

    def setup_layout(self):
        layout = QtWidgets.QVBoxLayout(self)

        layout.addWidget(
            self.label,
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.list,
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )

        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)