from PySide6 import QtWidgets

import database_controller
import report_generator


class SettlementDialog(QtWidgets.QDialog):
    """Dialog rozliczeniowy:
    wybór klienta -> produkt + platforma + wypłata -> raport PDF.
    """
    def __init__(self, parent=None, email_mode=False):
        super().__init__(parent)

        self.email_mode = email_mode
        if self.email_mode:
            self.setWindowTitle("Wybór danych do wiadomości e-mail")
        else:
            self.setWindowTitle("Nowe rozliczenie")
        self.resize(600, 500)

        self.clients = database_controller.load_database("clients")
        self.streamings = database_controller.load_database("streamings")
        self.products = database_controller.load_database("products")

        self.client_box = QtWidgets.QComboBox()

        for client in self.clients:
            self.client_box.addItem(
                f"{client['name']} (prowizja {client['cut']}%)",
                client["id"]
            )

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels([
            "Produkt",
            "Platforma",
            "Wypłata (zł)"
        ])
        self.table.setRowCount(1)
        self.add_empty_row(0)

        self.table.horizontalHeader().setStretchLastSection(True)

        if self.email_mode:
            self.generate_button = QtWidgets.QPushButton("Generuj PDF i załącz do e-maila")
        else:
            self.generate_button = QtWidgets.QPushButton("Generuj raport PDF")

        self.generate_button.clicked.connect(self.generate_report)

        self.setup_layout()

    def add_empty_row(self, row):
        product_box = QtWidgets.QComboBox()
        product_box.addItem("")

        for product in self.products:
            product_box.addItem(str(product["name"]), product["id"])

        platform_box = QtWidgets.QComboBox()
        platform_box.addItem("")

        for streaming in self.streamings:
            platform_box.addItem(str(streaming["name"]), streaming["id"])

        self.table.setCellWidget(row, 0, product_box)
        self.table.setCellWidget(row, 1, platform_box)
        self.table.setItem(row, 2, QtWidgets.QTableWidgetItem("0"))

        product_box.currentIndexChanged.connect(
            lambda _, r=row: self.check_new_row(r)
        )
        platform_box.currentIndexChanged.connect(
            lambda _, r=row: self.check_new_row(r)
        )

    def check_new_row(self, row):
        if row != self.table.rowCount() - 1:
            return

        product = self.table.cellWidget(row, 0)
        platform = self.table.cellWidget(row, 1)

        if (
                product
                and platform
                and product.currentIndex() > 0
                and platform.currentIndex() > 0
        ):
            new_row = self.table.rowCount()
            self.table.insertRow(new_row)
            self.add_empty_row(new_row)

    def collect_items(self):
        items = []

        for row in range(self.table.rowCount()):
            product_box = self.table.cellWidget(row, 0)
            platform_box = self.table.cellWidget(row, 1)

            if not product_box or product_box.currentIndex() == 0:
                continue

            table_item = self.table.item(row, 2)
            revenue_text = (
                table_item.text().replace(",", ".").strip()
                if table_item else "0"
            )

            try:
                revenue = float(revenue_text)
            except ValueError:
                raise ValueError("Niepoprawna kwota wypłaty.")

            product = database_controller.item_get(product_box.currentData(), "products")
            platform = database_controller.item_get(platform_box.currentData(), "streamings")

            items.append({
                "product": product,
                "platform": platform,
                "revenue": revenue
            })

        return items

    def generate_report(self):
        if not self.clients:
            QtWidgets.QMessageBox.warning(self, "Uwaga", "Brak klientów w bazie.")
            return

        client = database_controller.item_get(self.client_box.currentData(), "clients")

        try:
            items = self.collect_items()
        except ValueError as error:
            QtWidgets.QMessageBox.warning(self, "Uwaga", str(error))
            return

        if not items:
            QtWidgets.QMessageBox.warning(self, "Uwaga", "Dodaj przynajmniej jeden produkt.")
            return

        try:
            file_path = report_generator.generate_settlement_pdf(client, items)
            self.generated_file_path = file_path
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Uwaga", "Prowizja klienta i platformy musi być liczbą.")
            return

            # 5. BLOKUJEMY WYSKAKUJĄCY KOMUNIKAT, JEŚLI JESTEŚMY W TRYBIE EMAIL
        if not self.email_mode:
            QtWidgets.QMessageBox.information(self, "Gotowe", f"Zapisano raport:\n{file_path}")

        self.accept()

    def setup_layout(self):
        layout = QtWidgets.QVBoxLayout(self)

        layout.addWidget(QtWidgets.QLabel("Klient:"))
        layout.addWidget(self.client_box)
        layout.addWidget(
            QtWidgets.QLabel("Wybierz produkt, platformę i wpisz wypłatę:")
        )
        layout.addWidget(self.table)
        layout.addWidget(self.generate_button)
