from PyQt5.QtCore import (QDate, QDateTime, QRegExp, QSortFilterProxyModel, Qt,
                          QTime, Qt, QEvent, QObject)
from PyQt5 import QtPrintSupport
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
from typing import List
from data_models.recipe import Recipe
from support import gui_helpers
from gui_models.export_dialog import ExportDialog
from collections import namedtuple


class GuiState(object):
    def __init__(self):
        self.active_recipe = None
        self.active_meal_plan = None


class BaseGuiModel(object):
    recipes: List[Recipe] = []
    state = GuiState()

    def __init__(self, parent):
        # self.active_recipe = self.state.active_recipe
        # self.active_recipe =
        self.parent = parent
        self.model = None
        self.group_box = QGroupBox("")

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
        dialog = ExportDialog()
        dialog.exec()

    def set_recipe(self, recipe):
        self.state.active_recipe = recipe
        self.refresh()

    def refresh(self):
        raise NotImplementedError()

    def insert_row_at_end(self, data):
        idx = self.model.rowCount()
        self.model.insertRow(idx)

        if isinstance(data, list):
            for col_idx, column_data in enumerate(data):
                self.model.setData(
                    self.model.index(idx, col_idx),
                    column_data
                )
        else:
            self.model.setData(
                self.model.index(idx, 0),
                data
            )