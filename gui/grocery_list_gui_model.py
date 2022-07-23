import sys

from PyQt5.QtGui import QIcon, QStandardItemModel
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
                             QTreeView)
from PyQt5.QtCore import Qt
from gui.instructions_gui_model import InstructionsGuiModel
from gui.ingredients_gui_model import CenterPanelComponent
from gui.recipe_list_gui_model import RecipeListGuiModel
import config
from support import gui_helpers
import os
from gui.base_gui_model import BaseGuiModel
from gui.prints_and_exports import PrintsAndExports


class GroceryListGuiModel(BaseGuiModel):
    def __init__(self, parent):
        super().__init__(parent)
        self.model = gui_helpers.create_treeview_model(self.parent, ["Have it", "Item"])
        self.list_layout = QVBoxLayout()
        self.list_view = QTreeView()

        self.list_layout.addWidget(self.list_view)
        self.list_view.setAlternatingRowColors(True)
        self.list_view.setModel(self.model)

        self.add_btn = gui_helpers.create_tool_button("Add")
        # TODO: connect add grocery list item button
        self.add_btn.setToolTip(config.get_tooltip("add_instruction_button"))
        self.remove_btn = gui_helpers.create_tool_button("Remove")
        # TODO: connect remove grocery list item button
        self.remove_btn.setToolTip(config.get_tooltip("remove_instruction_button"))
        self.add_remove_btn_layout = QHBoxLayout()
        self.add_remove_btn_layout.setAlignment(Qt.AlignLeft)
        self.add_remove_btn_layout.addWidget(self.add_btn)
        self.add_remove_btn_layout.addWidget(self.remove_btn)
        self.button_layout = QHBoxLayout()
        self.button_layout.addLayout(self.add_remove_btn_layout)
        self.button_layout.addLayout(self.print_export_button_layout)
        self.list_layout.addLayout(self.button_layout)

        self.group_box.setLayout(self.list_layout)
        self.group_box.setMaximumWidth(1000)

    def refresh(self):
        ...