from PySide6 import QtWidgets, QtCore

from GUI.Widgets.CrudTable.CrudTable import CrudTable


class ProductsTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.productTable = CrudTable(["Id", "Title", "Author"], "products")
        self.searchBar = QtWidgets.QLineEdit()
        self.searchBar.setFixedWidth(200)
        self.searchBar.setPlaceholderText("Search here..")

        self.searchBar.textChanged.connect(
            self.productTable.table.search
        )

        layoutSearch = QtWidgets.QHBoxLayout()

        layoutSearch.addStretch()
        layoutSearch.addWidget(self.searchBar)
        layoutSearch.addStretch()

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(layoutSearch)
        layout.addWidget(self.productTable)

        self.setLayout(layout)


