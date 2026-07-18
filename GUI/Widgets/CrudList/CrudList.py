from PySide6 import QtWidgets, QtCore

from GUI.Widgets.Buttons.AddListButton import AddListButton
from GUI.Widgets.Buttons.RemoveListButton import RemoveListButton
from GUI.Widgets.CrudList.List import List
from GUI.Widgets.Buttons.AddTableButton import AddTableButton


class CrudList(QtWidgets.QWidget):
    def __init__(self, database_name):
        super().__init__()

        self.list = List(database_name)

        self.details = QtWidgets.QWidget()
        self.details.setFixedWidth(300)

        details_layout = QtWidgets.QFormLayout(self.details)

        self.id_label = QtWidgets.QLabel("-")
        self.name_edit = QtWidgets.QLineEdit()
        self.cut_edit = QtWidgets.QLineEdit()
        self.email_edit = QtWidgets.QLineEdit()

        details_layout.addRow("Id:", self.id_label)
        details_layout.addRow("Name:", self.name_edit)
        details_layout.addRow("Cut:", self.cut_edit)
        details_layout.addRow("Email:", self.email_edit)

        self.add_button = AddListButton(database_name, self.list.refresh_list)
        self.remove_button = RemoveListButton(database_name, self.list, self.list.refresh_list)

        self.list.selected.connect(self.show_details)

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






    def show_details(self, data):
        self.id_label.setText(str(data["id"]))
        self.name_edit.setText(data["name"])
        self.cut_edit.setText(str(data["cut"]))
        self.email_edit.setText(data.get("email", ""))