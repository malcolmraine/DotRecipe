# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import (Qt)
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QStandardItemModel
from PyQt5.QtWidgets import (QGroupBox, QHBoxLayout, QTreeView, QVBoxLayout,
                             QRadioButton, QLineEdit)
from support.gui_helpers import create_tool_button, create_label, create_treeview_model, get_icon
from gui.base_gui_model import BaseGuiModel
from gui.recipe_image import RecipeImage
from gui.base_gui_model import GuiState
import config
from gui.emg_base import EMGLineEdit, EMGTreeView, EMGRadioButton
from typing import Any
from data_models.ingredient import Ingredient
from data_models.quantity import Quantity

AMOUNT_COL_IDX = 0
NAME_COL_IDX = 1
NOTE_COL_IDX = 2


class IngredientItemModel(QStandardItemModel):
    def __init__(self, parent, headers, state: GuiState):
        super().__init__(0, len(headers), parent)
        self.state = state

        for idx, header in enumerate(headers):
            self.setHeaderData(idx, Qt.Horizontal, header)

    def setData(self, index: QtCore.QModelIndex, value: Any, role: int = Qt.EditRole) -> bool:
        print("Updating ingredients: ", value, index.row(), index.column())
        recipe = self.state.active_recipe
        ingredient = recipe.ingredients[index.row()]
        col = index.column()

        if col == AMOUNT_COL_IDX:
            ingredient.qty.from_nl_string(value)
            return super(IngredientItemModel, self).setData(index, ingredient.qty.as_fraction_string(), role)
        elif col == NAME_COL_IDX:
            ingredient.name = value
            return super(IngredientItemModel, self).setData(index, value, role)
        elif col == NOTE_COL_IDX:
            return super(IngredientItemModel, self).setData(index, value, role)

        return False

    def toFractionPres(self, index: QtCore.QModelIndex) -> bool:
        recipe = self.state.active_recipe
        ingredient = recipe.ingredients[index.row()]
        return super(IngredientItemModel, self).setData(index, ingredient.qty.as_fraction_string(), Qt.EditRole)

    def toFloatPres(self, index: QtCore.QModelIndex) -> bool:
        recipe = self.state.active_recipe
        ingredient = recipe.ingredients[index.row()]
        return super(IngredientItemModel, self).setData(index, ingredient.qty.as_fraction_string(), Qt.EditRole)


class IngredientsList(BaseGuiModel):

    def __init__(self, parent):
        super().__init__(parent)

        self.model = IngredientItemModel(parent, ["Qty", "Ingredient", "Notes"], self.state)
        self.list_layout = QVBoxLayout()
        self.list_view = self.make_listview()
        self.list_view.setModel(self.model)

        # self.list_layout.addWidget(self.recipe_image)
        self.list_layout.addWidget(self.list_view)
        self.add_remove_btn_layout = QHBoxLayout()
        self.add_ingredient_btn = create_tool_button("Add")
        self.add_ingredient_btn.clicked.connect(self.add_ingredient)
        self.add_ingredient_btn.setToolTip(config.get_tooltip("add_ingredient_button"))
        self.remove_ingredient_btn = create_tool_button("Remove")
        self.remove_ingredient_btn.clicked.connect(self.remove_ingredient)
        self.remove_ingredient_btn.setToolTip(config.get_tooltip("remove_ingredient_button"))
        self.metric_units_radio_btn = EMGRadioButton("Metric")
        self.us_units_radio_btn = EMGRadioButton("US", checked=True)

        self.lower_layout = QHBoxLayout()
        self.button_layout = QHBoxLayout()
        self.add_remove_btn_layout.setAlignment(Qt.AlignLeft)
        self.add_remove_btn_layout.addWidget(self.add_ingredient_btn)
        self.add_remove_btn_layout.addWidget(self.remove_ingredient_btn)
        self.add_remove_btn_layout.addWidget(self.metric_units_radio_btn)
        self.add_remove_btn_layout.addWidget(self.us_units_radio_btn)
        self.button_layout.addLayout(self.add_remove_btn_layout)

        self.servings_layout = QHBoxLayout()
        self.servings_layout.setAlignment(Qt.AlignRight)
        self.decrement_servings_btn = create_tool_button("")
        self.decrement_servings_btn.setIcon(get_icon("minus-sign.png"))
        self.decrement_servings_btn.clicked.connect(self.decrement_servings)
        self.increment_servings_btn = create_tool_button("")
        self.increment_servings_btn.setIcon(get_icon("plus.png"))
        self.increment_servings_btn.clicked.connect(self.increment_servings)
        self.servings_line_edit = EMGLineEdit(28, 35, "center", config.DEFAULT_SERVINGS_COUNT)
        self.servings_layout.addWidget(self.decrement_servings_btn)
        self.servings_layout.addWidget(self.servings_line_edit)
        self.servings_layout.addWidget(self.increment_servings_btn)

        self.lower_layout.addLayout(self.button_layout)
        self.lower_layout.addLayout(self.servings_layout)
        self.list_layout.addLayout(self.lower_layout)

    @staticmethod
    def make_listview():
        list_view = EMGTreeView()
        list_view.resizeColumnToContents(1)
        list_view.resizeColumnToContents(2)
        list_view.setRootIsDecorated(False)

        return list_view

    def increment_servings(self):
        current_servings = int(self.servings_line_edit.text())
        new_servings = current_servings + 1
        self.servings_line_edit.setText(str(new_servings))
        self.state.active_recipe.default_serving_qty = new_servings

        for ingredient in self.state.active_recipe.ingredients:
            ingredient.qty = (ingredient.qty / current_servings) * new_servings
        self.refresh()

    def decrement_servings(self):
        current_servings = int(self.servings_line_edit.text())
        new_servings = current_servings - 1

        if new_servings < 1:
            new_servings = 1
        self.servings_line_edit.setText(str(new_servings))
        self.state.active_recipe.default_serving_qty = new_servings

        for ingredient in self.state.active_recipe.ingredients:
            ingredient.qty = (ingredient.qty / current_servings) * new_servings
        self.refresh()

    def add_ingredient(self):
        ingredient = Ingredient()
        ingredient.name = "New Ingredient"
        ingredient.qty = Quantity(0)
        self.state.active_recipe.ingredients.append(ingredient)
        self.insert_row_at_end(["0", "New Ingredient", ""])


    def remove_ingredient(self):
        selected_indexes = self.list_view.selectedIndexes()

        if len(selected_indexes):
            self.model.removeRow(selected_indexes[0].row())

    def refresh(self):
        self.clear_listview_rows()
        for idx, ingredient in enumerate(self.state.active_recipe.ingredients):
            self.insert_row_at_end([
                ingredient.formatted_amount(),
                ingredient.name,
                ingredient.description
            ])

    def clear_listview_rows(self):
        self.model.removeRows(0, self.model.rowCount())