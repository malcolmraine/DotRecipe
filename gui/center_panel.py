# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QGroupBox, QHBoxLayout, QTreeView, QVBoxLayout,
                             QRadioButton, QLineEdit)
from support.gui_helpers import create_tool_button, create_label, create_treeview_model, get_icon
from gui.base_gui_model import BaseGuiModel
from gui.recipe_image import RecipeImage
import config
from gui.emg_base import EMGLineEdit, EMGTreeView, EMGRadioButton
from gui.ingredients_list import IngredientsList


class CenterPanelComponent(BaseGuiModel):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.recipe_image = RecipeImage(config.DEFAULT_IMAGE_PATH)
        self.layout.addWidget(self.recipe_image)
        self.ingredients_list = IngredientsList(parent)
        self.layout.addLayout(self.ingredients_list.list_layout)

        self.group_box.setLayout(self.layout)
        self.group_box.setMaximumWidth(600)

    def set_image(self):
        if self.state.active_recipe.image:
            self.recipe_image.setPixmap(QPixmap(self.state.active_recipe.image))
            self.recipe_image.setToolTip(self.state.active_recipe.title)
            self.recipe_image.image_save_name = self.state.active_recipe.image
        else:
            self.recipe_image.setPixmap(QPixmap(config.DEFAULT_IMAGE_PATH))
            self.recipe_image.setToolTip(config.get_tooltip("default_image"))
            self.recipe_image.image_save_name = "unknown"

    def refresh(self):
        print("Before set image ", [self.state.active_recipe.image, self.state.active_recipe.title])
        self.set_image()
        self.ingredients_list.refresh()