from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (
    QLabel,
    QToolButton,
)

from support.path_helpers import make_icon_path


def create_tool_button(text):
    btn = QToolButton()
    btn.setText(text)

    return btn


def create_treeview_model(parent, headers):
    model = QStandardItemModel(0, len(headers), parent)

    for idx, header in enumerate(headers):
        model.setHeaderData(idx, Qt.Horizontal, header)

    return model


def create_label(text):
    label = QLabel(text)


def get_icon(name: str) -> QIcon:
    return QIcon(make_icon_path(name))
