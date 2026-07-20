import os
import json
from PySide6 import QtWidgets

DB_DIR = "Databases"
os.makedirs(DB_DIR, exist_ok=True)
CUSTOM_EMAILS_FILE = os.path.join(DB_DIR, "custom_emails.json")

class CustomEmailsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Zarządzaj własnymi mailami")
        self.resize(400, 300)
        layout = QtWidgets.QHBoxLayout(self)

        self.list_widget = QtWidgets.QListWidget()
        layout.addWidget(self.list_widget)

        buttons_layout = QtWidgets.QVBoxLayout()

        self.add_button = QtWidgets.QPushButton("Dodaj nowy")
        self.add_button.clicked.connect(self.add_email)

        self.edit_button = QtWidgets.QPushButton("Edytuj zaznaczony")
        self.edit_button.clicked.connect(self.edit_email)

        self.delete_button = QtWidgets.QPushButton("Usuń zaznaczony")
        self.delete_button.clicked.connect(self.delete_email)

        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addStretch()

        layout.addLayout(buttons_layout)

        self.load_emails()

    def load_emails(self):
        self.list_widget.clear()
        if os.path.exists(CUSTOM_EMAILS_FILE):
            try:
                with open(CUSTOM_EMAILS_FILE, "r", encoding="utf-8") as f:
                    emails = json.load(f)
                    for email in emails:
                        self.list_widget.addItem(email)
            except Exception:
                pass

    def save_emails(self):
        emails = [self.list_widget.item(i).text() for i in range(self.list_widget.count())]
        try:
            with open(CUSTOM_EMAILS_FILE, "w", encoding="utf-8") as f:
                json.dump(emails, f, indent=4, ensure_ascii=False)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas zapisywania: {e}")

    def add_email(self):
        email, ok = QtWidgets.QInputDialog.getText(self, "Dodaj e-mail", "Podaj własny adres e-mail:")
        if ok and email.strip():
            email = email.strip()
            existing = [self.list_widget.item(i).text() for i in range(self.list_widget.count())]
            if email not in existing:
                self.list_widget.addItem(email)
                self.save_emails()
            else:
                QtWidgets.QMessageBox.information(self, "Informacja", "Ten adres e-mail jest już na liście.")

    def edit_email(self):
        selected_item = self.list_widget.currentItem()
        if not selected_item:
            QtWidgets.QMessageBox.warning(self, "Błąd",
                                          "Wybierz najpierw adres z listy po lewej stronie, który chcesz edytować.")
            return

        current_email = selected_item.text()
        new_email, ok = QtWidgets.QInputDialog.getText(self, "Edytuj e-mail", "Zmień adres e-mail:", text=current_email)

        if ok and new_email.strip():
            new_email = new_email.strip()
            if new_email == current_email:
                return

            existing = [self.list_widget.item(i).text() for i in range(self.list_widget.count())]
            if new_email in existing:
                QtWidgets.QMessageBox.information(self, "Informacja", "Ten adres e-mail już istnieje na liście.")
                return

            selected_item.setText(new_email)
            self.save_emails()

    def delete_email(self):
        selected_item = self.list_widget.currentItem()
        if not selected_item:
            QtWidgets.QMessageBox.warning(self, "Błąd",
                                          "Wybierz najpierw adres z listy po lewej stronie, który chcesz usunąć.")
            return

        current_email = selected_item.text()
        odpowiedz = QtWidgets.QMessageBox.question(
            self,
            "Potwierdzenie usunięcia",
            f"Czy na pewno chcesz usunąć adres:\n{current_email}?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )

        if odpowiedz == QtWidgets.QMessageBox.StandardButton.Yes:
            self.list_widget.takeItem(self.list_widget.row(selected_item))
            self.save_emails()