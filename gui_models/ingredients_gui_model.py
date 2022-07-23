# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QGroupBox, QHBoxLayout, QTreeView, QVBoxLayout,
                             QRadioButton, QLineEdit)
from support.gui_helpers import create_tool_button, create_label, create_treeview_model, get_icon
from gui_models.base_gui_model import BaseGuiModel
from recipe_image import RecipeImage
import config
from gui_models.emg_base import EMGLineEdit, EMGTreeView, EMGRadioButton


class IngredientsGuiModel(BaseGuiModel):
    def __init__(self, parent):
        super().__init__(parent)
        self.model = create_treeview_model(parent, ["Qty", "Ingredient", "Notes"])
        self.food_img_label = RecipeImage(config.DEFAULT_IMAGE_PATH)
        self.food_img_label.setAlignment(Qt.AlignCenter)
        self.list_layout = QVBoxLayout()
        self.list_view = self.make_listview()
        self.list_view.setModel(self.model)

        self.list_layout.addWidget(self.food_img_label)
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

        self.group_box.setLayout(self.list_layout)
        self.group_box.setMaximumWidth(600)

    def increment_servings(self):
        current_servings = int(self.servings_line_edit.text())
        self.servings_line_edit.setText(str(current_servings + 1))
        # TODO: Recalculate ingredients

    def decrement_servings(self):
        current_servings = int(self.servings_line_edit.text())
        new_servings = current_servings - 1

        if new_servings < 1:
            new_servings = 1
        self.servings_line_edit.setText(str(new_servings))
        # TODO: Recalculate ingredients

    def clear_listview_rows(self):
        self.model.removeRows(0, self.model.rowCount())

    def set_image(self):
        if self.state.active_recipe.image:
            self.food_img_label.setPixmap(QPixmap(self.state.active_recipe.image))
            self.food_img_label.setToolTip(self.state.active_recipe.title)
            self.food_img_label.image_save_name = self.state.active_recipe.image
        else:
            self.food_img_label.setPixmap(QPixmap(config.DEFAULT_IMAGE_PATH))
            self.food_img_label.setToolTip(config.get_tooltip("default_image"))
            self.food_img_label.image_save_name = "unknown"

    @staticmethod
    def make_listview():
        list_view = EMGTreeView()
        list_view.resizeColumnToContents(1)
        list_view.resizeColumnToContents(2)
        list_view.setRootIsDecorated(False)

        return list_view

    def refresh(self):
        self.clear_listview_rows()
        self.set_image()

        for idx, ingredient in enumerate(self.state.active_recipe.ingredients):
            self.insert_row_at_end([
                ingredient.formatted_amount(),
                ingredient.name,
                ingredient.description
            ])

    def add_ingredient(self):
        self.insert_row_at_end(["0", "New Ingredient", ""])

    def remove_ingredient(self):
        selected_indexes = self.list_view.selectedIndexes()

        if len(selected_indexes):
            self.model.removeRow(selected_indexes[0].row())