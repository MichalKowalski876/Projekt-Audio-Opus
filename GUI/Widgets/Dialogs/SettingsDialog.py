import os
import json
from PySide6 import QtWidgets

DB_DIR = "Databases"
os.makedirs(DB_DIR, exist_ok=True)
SMTP_CONFIG_FILE = os.path.join(DB_DIR, "smtp_config.json")
MSG_CONFIG_FILE = os.path.join(DB_DIR, "msg_config.json")

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ustawienia poczty i wiadomości")
        self.setMinimumSize(450, 450)

        main_layout = QtWidgets.QVBoxLayout(self)

        smtp_group = QtWidgets.QGroupBox("Ustawienia serwera SMTP")
        smtp_layout = QtWidgets.QFormLayout()

        self.server_input = QtWidgets.QLineEdit()
        self.port_input = QtWidgets.QLineEdit()
        self.sender_email_input = QtWidgets.QLineEdit()
        self.sender_password_input = QtWidgets.QLineEdit()
        self.sender_password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        smtp_layout.addRow("Serwer SMTP:", self.server_input)
        smtp_layout.addRow("Port SMTP:", self.port_input)
        smtp_layout.addRow("Twój E-mail:", self.sender_email_input)
        smtp_layout.addRow("Hasło (App Password):", self.sender_password_input)
        smtp_group.setLayout(smtp_layout)

        msg_group = QtWidgets.QGroupBox("Szablon wiadomości")
        msg_layout = QtWidgets.QFormLayout()

        self.subject_input = QtWidgets.QLineEdit()
        self.body_input = QtWidgets.QTextEdit()
        self.body_input.setMinimumHeight(150)

        msg_layout.addRow("Temat maila:", self.subject_input)
        msg_layout.addRow("Treść maila:", self.body_input)
        msg_group.setLayout(msg_layout)

        main_layout.addWidget(smtp_group)
        main_layout.addWidget(msg_group)

        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Save |
            QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.save_settings)
        self.button_box.rejected.connect(self.reject)

        main_layout.addWidget(self.button_box)

        self.load_settings()

    def load_settings(self):
        if os.path.exists(SMTP_CONFIG_FILE):
            try:
                with open(SMTP_CONFIG_FILE, "r", encoding="utf-8") as f:
                    smtp_config = json.load(f)
                    self.server_input.setText(smtp_config.get("SMTP_SERVER", "smtp.gmail.com"))
                    self.port_input.setText(str(smtp_config.get("SMTP_PORT", 465)))
                    self.sender_email_input.setText(smtp_config.get("SENDER_EMAIL", ""))
                    self.sender_password_input.setText(smtp_config.get("SENDER_PASSWORD", ""))
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Błąd", f"Nie udało się wczytać ustawień SMTP: {e}")
        else:
            self.server_input.setText("smtp.gmail.com")
            self.port_input.setText("465")

        default_subject = "Zbiorczy raport rozliczeniowy Audio Opus"
        default_body = "Dzień dobry,\n\nW załączniku znajduje się aktualny raport rozliczeniowy wygenerowany przez system Audio Opus."

        if os.path.exists(MSG_CONFIG_FILE):
            try:
                with open(MSG_CONFIG_FILE, "r", encoding="utf-8") as f:
                    msg_config = json.load(f)
                    self.subject_input.setText(msg_config.get("EMAIL_SUBJECT", default_subject))
                    self.body_input.setPlainText(msg_config.get("EMAIL_BODY", default_body))
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Błąd", f"Nie udało się wczytać ustawień wiadomości: {e}")
        else:
            self.subject_input.setText(default_subject)
            self.body_input.setPlainText(default_body)

    def save_settings(self):
        smtp_config = {
            "SMTP_SERVER": self.server_input.text().strip(),
            "SMTP_PORT": self.port_input.text().strip(),
            "SENDER_EMAIL": self.sender_email_input.text().strip(),
            "SENDER_PASSWORD": self.sender_password_input.text().strip()
        }

        msg_config = {
            "EMAIL_SUBJECT": self.subject_input.text().strip(),
            "EMAIL_BODY": self.body_input.toPlainText().strip()
        }

        try:
            with open(SMTP_CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(smtp_config, f, indent=4, ensure_ascii=False)

            with open(MSG_CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(msg_config, f, indent=4, ensure_ascii=False)

            QtWidgets.QMessageBox.information(self, "Sukces", "Ustawienia zostały pomyślnie zapisane!")
            self.accept()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas zapisywania: {e}")
