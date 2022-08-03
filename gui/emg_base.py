import sys

from PyQt5.QtGui import QIcon, QStandardItemModel
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtGui import QCursor
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
    QMenu,
    QRadioButton,
    QMessageBox,
    QLineEdit,
)
import config
from support import gui_helpers
import os


class EMGTreeView(QTreeView):
    def __init__(self):
        super().__init__()

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        menu = QMenu(self)
        remove_action = menu.addAction("Remove")
        print_action = menu.addAction("Print")
        action = menu.exec_(self.mapToGlobal(event.pos()))


class EMGLineEdit(QLineEdit):
    def __init__(self, width: int, height: int, align="right", default=""):
        super().__init__()
        self.setMinimumWidth(width)
        self.setMaximumWidth(width)
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)
        self.setText(str(default))

        if align == "center":
            self.setAlignment(Qt.AlignCenter)
        elif align == "right":
            self.setAlignment(Qt.AlignRight)
        elif align == "left":
            self.setAlignment(Qt.AlignLeft)


class EMGRadioButton(QRadioButton):
    def __init__(self, *args, checked=False):
        super().__init__(*args)
        self.setChecked(checked)


class EMGMessageBox(QMessageBox):
    def __init__(self, *args):
        super().__init__(*args)

    @staticmethod
    def confirm(parent, title, text):
        box = EMGMessageBox()
        ret = box.question(parent, title, text, box.Yes | box.No)

        return ret == box.Yes

    @staticmethod
    def info(parent, title, text):
        box = EMGMessageBox()
        box.question(parent, title, text, box.Ok)
