import sys
from typing import Dict
from PyQt5.QtGui import QIcon, QStandardItemModel
from PyQt5.QtCore import Qt
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
# from gui_models.instructions_gui_model import InstructionsGuiModel
# from gui_models.ingredients_gui_model import IngredientsGuiModel
# from gui_models.recipe_list_gui_model import RecipeListGuiModel
import config
from support import gui_helpers
import os
from gui_models.base_gui_model import BaseGuiModel


class MealPlanGuiModel(BaseGuiModel):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_layout = QVBoxLayout()
        meal_plan_table = QTableView()
        self.main_layout.addWidget(meal_plan_table)

        self.button_layout = QHBoxLayout()
        self.button_layout.setAlignment(Qt.AlignLeft)
        self.save_btn = gui_helpers.create_tool_button("Save")
        self.save_btn.setToolTip(config.get_tooltip("save_meal_plan_button"))
        self.button_layout.addWidget(self.save_btn)
        self.reset_btn = gui_helpers.create_tool_button("Reset")
        self.reset_btn.setToolTip(config.get_tooltip("reset_meal_plan_button"))
        self.button_layout.addWidget(self.reset_btn)
        self.main_layout.addLayout(self.button_layout)
        table_model = QStandardItemModel(0, 7, self.parent)
        meal_plan_table.setModel(table_model)
        table_model.setHorizontalHeaderLabels(config.WEEKDAYS)
        table_model.setVerticalHeaderLabels([
            "Meals",
            "Notes",
        ])

        for n in range(7):
            meal_plan_table.setColumnWidth(n, 200)

        meal_plan_table.setRowHeight(0, 100)
        meal_plan_table.setRowHeight(1, 250)
        self.meals_combos: Dict[str, QComboBox] = {}

        for idx, day in enumerate(config.WEEKDAYS):
            combo = self.make_meal_combo()
            meal_plan_table.setIndexWidget(table_model.index(0, idx), combo)
            self.meals_combos[day] = combo

        self.group_box.setLayout(self.main_layout)
        self.group_box.setMaximumWidth(2000)

    def make_meal_combo(self):
        combo = QComboBox()
        combo.addItem("--  Meal  --")
        combo.addItems([recipe.title for recipe in self.recipes])
        return combo

    def refresh(self):
        for combo in self.meals_combos.items():
            combo[1].clear()
            combo[1].addItems([recipe.title for recipe in self.recipes])