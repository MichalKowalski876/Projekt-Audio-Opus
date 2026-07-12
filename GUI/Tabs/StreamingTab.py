from PySide6 import QtWidgets

import report_generator
from GUI.Widgets.CrudTable.CrudTable import CrudTable
from GUI.Widgets.Settlement.SettlementDialog import SettlementDialog

KNOWN_STREAMINGS = [
    "Audioteka",
    "Empik Go",
    "Legimi",
    "BookBeat",
    "Storytel",
    "Audible",
    "Spotify"
]


class StreamingTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.crudTable = CrudTable(
            ["Id", "Name", "Cut"],
            "streamings",
            {"name": KNOWN_STREAMINGS},
            field_types={"cut":float}
        )

        self.settlement_button = QtWidgets.QPushButton("Nowe rozliczenie (PDF)")
        self.settlement_button.clicked.connect(self.open_settlement)

        self.report_button = QtWidgets.QPushButton("Raport platform (TXT)")
        self.report_button.clicked.connect(self.generate_streamings_report)

        self.setup_layout()

    def open_settlement(self):
        dialog = SettlementDialog(self)
        dialog.exec()

    def generate_streamings_report(self):
        file_path = report_generator.generate_streamings_report()

        QtWidgets.QMessageBox.information(
            self,
            "Gotowe",
            "Zapisano raport:\n" + file_path
        )

    def setup_layout(self):
        reports_layout = QtWidgets.QVBoxLayout()
        reports_layout.addWidget(self.settlement_button)
        reports_layout.addWidget(self.report_button)
        reports_layout.addStretch()

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.crudTable)
        layout.addLayout(reports_layout)
