import sys

from PyQt5.QtGui import QIcon, QStandardItemModel
from PyQt5 import QtPrintSupport
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
)
from PyQt5.QtCore import Qt
from support import gui_helpers
from gui.export_dialog import ExportDialog


class PrintsAndExports(object):
    def __init__(self):
        self.print_export_button_layout = QHBoxLayout()
        self.print_export_button_layout.setAlignment(Qt.AlignRight)
        self.export_button = gui_helpers.create_tool_button("Export")
        self.export_button.clicked.connect(self.handle_export)
        self.print_export_button_layout.addWidget(self.export_button)
        self.print_button = gui_helpers.create_tool_button("Print")
        self.print_button.clicked.connect(self.handle_print)
        self.print_export_button_layout.addWidget(self.print_button)

    def handle_print(self):
        printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
        dialog = QtPrintSupport.QPrintDialog(printer)
        if dialog.exec_() == QtPrintSupport.QPrintDialog.Accepted:
            ...

    def handle_export(self):
        dialog = ExportDialog(self.parent, self.state)
        dialog.exec()
