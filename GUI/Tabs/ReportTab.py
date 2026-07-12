from PySide6 import QtWidgets, QtCore
import email_sender
import report_generator

class ReportTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout(self)

        self.info_label = QtWidgets.QLabel("Wpisz adres e-mail, na który ma zostać wysłany raport")
        self.email_input = QtWidgets.QLineEdit()
        self.email_input.setPlaceholderText("np. xxxx@gmail.com")
        
        self.send_button = QtWidgets.QPushButton("Wyślij Raport")
        self.send_button.clicked.connect(self.on_send_clicked)

        layout.addWidget(self.info_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.send_button)
        layout.addStretch() 

    def on_send_clicked(self):
        receiver_email = self.email_input.text().strip()

        if not receiver_email:
            QtWidgets.QMessageBox.warning(self, "Błąd", "Proszę wpisać adres e-mail przed wysłaniem!")
            return

        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.WaitCursor)

        try:
            report_path = report_generator.generate_streamings_report()
            success = email_sender.send_report_email(receiver_email, report_path)

            QtWidgets.QApplication.restoreOverrideCursor()

            if success:
                QtWidgets.QMessageBox.information(
                    self, 
                    "Sukces", 
                    f"Raport został wygenerowany i pomyślnie wysłany na adres:\n{receiver_email}"
                )
                self.email_input.clear()
            else:
                QtWidgets.QMessageBox.critical(
                    self, 
                    "Błąd", 
                    "Nie udało się wysłać e-maila. Sprawdź konsolę lub konfigurację SMTP."
                )

        except Exception as e:
            QtWidgets.QApplication.restoreOverrideCursor()
            QtWidgets.QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas generowania raportu: {e}")