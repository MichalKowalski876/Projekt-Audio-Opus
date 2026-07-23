from PySide6 import QtWidgets

from GUI.Widgets.CrudTable.CrudTable import CrudTable


class ProductsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.productTable = CrudTable(["Id", "Title", "Author"], "products")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.productTable)

        self.setLayout(layout)
