import sys

from PyQt5.QtGui import QIcon, QStandardItemModel
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
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
)
from gui.instructions_gui_model import InstructionsGuiModel
from gui.center_panel import CenterPanelComponent
from gui.recipe_list_gui_model import RecipeListGuiModel
import config
from support import gui_helpers
import os
from gui.base_gui_model import BaseGuiModel
from gui.emg_base import EMGTreeView


class MealPlanListGuiModel(BaseGuiModel):
    def __init__(self, parent):
        super().__init__(parent)
        self.list_layout = QVBoxLayout()
        self.list_view = EMGTreeView()
        self.list_layout.addWidget(self.list_view)
        self.model = gui_helpers.create_treeview_model(
            self.parent, ["Plan Name", "Date"]
        )
        self.list_view.setAlternatingRowColors(True)
        self.list_view.setModel(self.model)

        self.add_btn = gui_helpers.create_tool_button("Add")
        # self.add_btn.clicked.connect(self.add_instruction)
        self.add_btn.setToolTip(config.get_tooltip("add_instruction_button"))
        self.remove_btn = gui_helpers.create_tool_button("Remove")
        # self.remove_btn.clicked.connect(self.remove_instruction)
        self.remove_btn.setToolTip(config.get_tooltip("remove_instruction_button"))
        self.add_remove_btn_layout = QHBoxLayout()
        self.add_remove_btn_layout.setAlignment(Qt.AlignLeft)
        self.add_remove_btn_layout.addWidget(self.add_btn)
        self.add_remove_btn_layout.addWidget(self.remove_btn)
        self.list_layout.addLayout(self.add_remove_btn_layout)

        self.group_box.setLayout(self.list_layout)
        self.group_box.setMaximumWidth(1000)

    def refresh(self):
        pass
