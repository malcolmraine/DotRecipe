from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMainWindow, QPushButton
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QTabWidget,
    QTableWidget,
    QTableView,
    QToolButton,
    QComboBox,
    QListView,
    QTreeView,
    QGroupBox,
)
from PyQt5.QtCore import (
    QDate,
    QDateTime,
    QRegExp,
    QSortFilterProxyModel,
    QTime,
    Qt,
    QEvent,
    QObject,
)
from support import gui_helpers
from gui.bubble_notification import ToastNotification


class ExportDialog(QDialog):
    def __init__(self, parent, state):
        super().__init__(parent)
        self.state = state
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.export_combo = QComboBox()
        self.export_combo.addItems(
            [
                "HTML",
                "PDF",
                # "Microsoft To-Do",
            ]
        )
        main_layout.addWidget(self.export_combo)
        self.export_btn = gui_helpers.create_tool_button("Export")
        self.export_btn.clicked.connect(self.handle_create)
        self.cancel_btn = gui_helpers.create_tool_button("Cancel")
        self.cancel_btn.clicked.connect(self.handle_cancel)
        self.export_cancel_layout = QHBoxLayout()
        self.export_cancel_layout.addWidget(self.export_btn)
        self.export_cancel_layout.addWidget(self.cancel_btn)
        self.export_cancel_layout.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        main_layout.addLayout(self.export_cancel_layout)
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)

    def handle_create(self):
        ...

    def handle_cancel(self):
        self.close()