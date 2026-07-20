import os
import json
from PySide6 import QtWidgets, QtCore
import email_sender
import database_controller
from GUI.Widgets.Settlement.SettlementDialog import SettlementDialog
from GUI.Widgets.Dialogs.SettingsDialog import SettingsDialog, SMTP_CONFIG_FILE
from GUI.Widgets.Dialogs.CustomEmailsDialog import CustomEmailsDialog, CUSTOM_EMAILS_FILE


class EmailComboBox(QtWidgets.QComboBox):
    def __init__(self, refresh_callback, parent=None):
        super().__init__(parent)
        self.refresh_callback = refresh_callback

    def showPopup(self):
        if self.refresh_callback:
            self.refresh_callback()
        super().showPopup()


class ReportTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout(self)

        self.info_label = QtWidgets.QLabel("Wpisz adres e-mail, na który ma zostać wysłany raport z rozliczeniem:")

        self.email_input = EmailComboBox(self.load_client_emails)
        self.email_input.setEditable(True)
        self.email_input.lineEdit().setPlaceholderText("np. xxxx@gmail.com lub wybierz z listy...")

        self.load_client_emails()

        self.send_button = QtWidgets.QPushButton("Wybierz dane i Wyślij Raport")
        self.send_button.clicked.connect(self.on_send_clicked)

        self.settings_button = QtWidgets.QPushButton("Ustawienia SMTP i Wiadomości")
        self.settings_button.clicked.connect(self.open_settings)

        self.manage_emails_button = QtWidgets.QPushButton("Zarządzaj własnymi adresami e-mail")
        self.manage_emails_button.clicked.connect(self.open_custom_emails_manager)

        layout.addWidget(self.info_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.send_button)
        layout.addSpacing(15)
        layout.addWidget(self.settings_button)
        layout.addSpacing(15)
        layout.addWidget(self.manage_emails_button)
        layout.addStretch()

    def load_client_emails(self):
        current_text = self.email_input.currentText()
        self.email_input.clear()

        try:
            clients = database_controller.load_database("clients")
            for client in clients:
                email = client.get("email")
                if not email:
                    email = client.get("Email")
                if email and isinstance(email, str):
                    email = email.strip()
                    if email:
                        self.email_input.addItem(email)
        except Exception as e:
            print(f"Błąd podczas ładowania bazy klientów: {e}")

        if os.path.exists(CUSTOM_EMAILS_FILE):
            try:
                with open(CUSTOM_EMAILS_FILE, "r", encoding="utf-8") as f:
                    custom_emails = json.load(f)
                    for custom_email in custom_emails:
                        if custom_email not in [self.email_input.itemText(i) for i in range(self.email_input.count())]:
                            self.email_input.addItem(custom_email)
            except Exception as e:
                print(f"Błąd podczas wczytywania własnych maili: {e}")

        if current_text:
            self.email_input.setCurrentText(current_text)
        else:
            self.email_input.setCurrentIndex(-1)

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec()

    def open_custom_emails_manager(self):
        dialog = CustomEmailsDialog(self)
        dialog.exec()
        self.load_client_emails()

    def on_send_clicked(self):
        receiver_email = self.email_input.currentText().strip()

        if not receiver_email:
            QtWidgets.QMessageBox.warning(self, "Błąd", "Proszę wpisać lub wybrać adres e-mail przed wysłaniem!")
            return

        if not os.path.exists(SMTP_CONFIG_FILE):
            QtWidgets.QMessageBox.warning(self, "Brak ustawień",
                                          "Proszę najpierw kliknąć 'Ustawienia SMTP i Wiadomości', aby skonfigurować pocztę wychodzącą.")
            return

        dialog = SettlementDialog(self, email_mode=True)
        result = dialog.exec()

        if result == QtWidgets.QDialog.DialogCode.Accepted:
            report_path = getattr(dialog, 'generated_file_path', None)

            if not report_path or not os.path.exists(report_path):
                QtWidgets.QMessageBox.critical(self, "Błąd",
                                               "Nie udało się odnaleźć wygenerowanego pliku PDF. Wysyłanie przerwane.")
                return

            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.WaitCursor)
            try:
                success = email_sender.send_report_email(receiver_email, report_path)
                QtWidgets.QApplication.restoreOverrideCursor()

                if success:
                    QtWidgets.QMessageBox.information(self, "Sukces",
                                                      f"Raport PDF został pomyślnie wygenerowany i wysłany na adres:\n{receiver_email}")
                    self.email_input.setCurrentText("")
                    self.email_input.setCurrentIndex(-1)
                else:
                    QtWidgets.QMessageBox.critical(self, "Błąd",
                                                   "Nie udało się wysłać e-maila. Sprawdź, czy dane uwierzytelniające w ustawieniach są poprawne.")

            except Exception as e:
                QtWidgets.QApplication.restoreOverrideCursor()
                QtWidgets.QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas wysyłania: {e}")

            finally:
                if os.path.exists(report_path):
                    try:
                        os.remove(report_path)
                    except Exception as e:
                        print(f"Nie udało się usunąć pliku tymczasowego: {e}")
