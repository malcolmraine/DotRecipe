from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton
from PyQt5.QtWidgets import (QApplication,
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
                             QGroupBox)


class ExportDialog(QDialog):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        main_layout.addWidget(QTreeView())
