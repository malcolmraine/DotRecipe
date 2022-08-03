# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtGui import QIcon, QStandardItemModel
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
    QMainWindow,
)
from gui.instructions_gui_model import InstructionsGuiModel
from gui.center_panel import CenterPanelComponent
from gui.recipe_list_gui_model import RecipeListGuiModel
from gui.meal_plan_gui_model import MealPlanGuiModel
from gui.meal_plan_list_gui_model import MealPlanListGuiModel
from gui.grocery_list_gui_model import GroceryListGuiModel
import config
from support import gui_helpers
import os


class App(QWidget):
    current_idx = None

    def __init__(self):
        super().__init__()
        self.title = config.APP_TITLE
        self.left = 10
        self.top = 10
        self.width = 2000
        self.height = 1600
        self.recipe_gui_model = RecipeListGuiModel(self)
        self.instructions_gui_model = InstructionsGuiModel(self)
        self.ingredients_gui_model = CenterPanelComponent(self)
        self.meal_plan_gui_model = MealPlanGuiModel(self)
        self.meal_plan_list_gui_model = MealPlanListGuiModel(self)
        self.grocery_list_gui_model = GroceryListGuiModel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        main_layout = QHBoxLayout()

        self.tabs = QTabWidget()
        self.recipes_tab = QWidget()
        self.meal_planning_tab = QWidget()
        self.tabs.resize(self.width, self.height)
        self.tabs.tabBarClicked.connect(self.grocery_list_gui_model.refresh)

        # Add tabs
        self.tabs.addTab(self.recipes_tab, "Recipes")
        self.tabs.addTab(self.meal_planning_tab, "Meal Planning")

        recipe_layout = QHBoxLayout()
        recipe_layout.addWidget(self.recipe_gui_model.group_box)
        recipe_layout.addWidget(self.ingredients_gui_model.group_box)
        recipe_layout.addWidget(self.instructions_gui_model.group_box)
        self.recipes_tab.layout = recipe_layout
        self.recipes_tab.setLayout(self.recipes_tab.layout)
        self.recipe_gui_model.load_recipes()

        meal_plan_layout = QVBoxLayout()
        upper_layout = QHBoxLayout()
        upper_layout.addWidget(self.meal_plan_list_gui_model.group_box)
        upper_layout.addWidget(self.grocery_list_gui_model.group_box)
        meal_plan_layout.addLayout(upper_layout)
        meal_plan_layout.addWidget(self.meal_plan_gui_model.group_box)
        self.meal_planning_tab.layout = meal_plan_layout
        self.meal_planning_tab.setLayout(self.meal_planning_tab.layout)

        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
        self.showMaximized()

    def load_active_recipe(self):
        self.recipe_gui_model.get_selected_recipe()
        self.instructions_gui_model.refresh()
        self.ingredients_gui_model.refresh()

    def refresh(self):
        self.meal_plan_gui_model.refresh()
        self.recipe_gui_model.refresh()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(config.APP_ICON))
    app.setStyle("Breeze")
    main_window = QMainWindow()
    menu_bar = main_window.menuBar()
    menu_bar.addMenu("&File")
    menu_bar.addMenu("&Edit")
    menu_bar.addMenu("&View")
    menu_bar.addMenu("&About")
    main_layout = QVBoxLayout()
    main_layout.addWidget(App())

    ex = main_window
    sys.exit(app.exec_())
