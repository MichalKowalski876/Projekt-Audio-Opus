from PySide6 import QtWidgets, QtCore

import database_controller
import report_generator


class SettlementDialog(QtWidgets.QDialog):
    """
    Dialog rozliczeniowy:
    wybór klienta -> wybór platform + wpisanie przychodu -> raport PDF.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Nowe rozliczenie")
        self.resize(600, 500)

        self.clients = database_controller.load_database("clients")
        self.streamings = database_controller.load_database("streamings")

        self.client_box = QtWidgets.QComboBox()
        for client in self.clients:
            self.client_box.addItem(
                str(client["name"]) + " (prowizja " + str(client["cut"]) + "%)",
                client["id"]
            )

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "",
            "Platforma",
            "Prowizja platformy",
            "Wypłata (zł)"
        ])

        self.table.setRowCount(len(self.streamings))

        for row, streaming in enumerate(self.streamings):
            check = QtWidgets.QTableWidgetItem()
            check.setFlags(
                QtCore.Qt.ItemFlag.ItemIsUserCheckable
                | QtCore.Qt.ItemFlag.ItemIsEnabled
            )
            check.setCheckState(QtCore.Qt.CheckState.Unchecked)
            self.table.setItem(row, 0, check)

            name = QtWidgets.QTableWidgetItem(str(streaming["name"]))
            name.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.table.setItem(row, 1, name)

            cut = QtWidgets.QTableWidgetItem(str(streaming["cut"]) + "%")
            cut.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.table.setItem(row, 2, cut)

            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem("0"))

        self.table.setColumnWidth(0, 30)
        self.table.horizontalHeader().setStretchLastSection(True)

        self.generate_button = QtWidgets.QPushButton("Generuj raport PDF")
        self.generate_button.clicked.connect(self.generate_report)

        self.setup_layout()

    def collect_items(self):
        items = []

        for row, streaming in enumerate(self.streamings):
            if self.table.item(row, 0).checkState() != QtCore.Qt.CheckState.Checked:
                continue

            revenue_text = self.table.item(row, 3).text().replace(",", ".").strip()

            try:
                revenue = float(revenue_text)
            except ValueError:
                raise ValueError(
                    "Niepoprawna wypłata dla platformy: " + str(streaming["name"])
                )

            items.append({
                "platform": streaming,
                "revenue": revenue
            })

        return items

    def generate_report(self):
        if not self.clients:
            QtWidgets.QMessageBox.warning(self, "Uwaga", "Brak klientów w bazie.")
            return

        client = database_controller.item_get(
            self.client_box.currentData(),
            "clients"
        )

        try:
            items = self.collect_items()
        except ValueError as error:
            QtWidgets.QMessageBox.warning(self, "Uwaga", str(error))
            return

        if not items:
            QtWidgets.QMessageBox.warning(
                self,
                "Uwaga",
                "Zaznacz przynajmniej jedną platformę."
            )
            return

        try:
            file_path = report_generator.generate_settlement_pdf(client, items)
        except ValueError:
            QtWidgets.QMessageBox.warning(
                self,
                "Uwaga",
                "Prowizja klienta i platformy musi być liczbą."
            )
            return

        QtWidgets.QMessageBox.information(
            self,
            "Gotowe",
            "Zapisano raport:\n" + file_path
        )

        self.accept()

    def setup_layout(self):
        layout = QtWidgets.QVBoxLayout(self)

        layout.addWidget(QtWidgets.QLabel("Klient:"))
        layout.addWidget(self.client_box)

        layout.addWidget(QtWidgets.QLabel(
            "Zaznacz platformy i wpisz wypłatę od każdej z nich:"
        ))
        layout.addWidget(self.table)

        layout.addWidget(self.generate_button)
