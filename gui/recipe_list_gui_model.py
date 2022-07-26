# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QComboBox, QGroupBox, QHBoxLayout, QLabel, QTreeView, QVBoxLayout, QMessageBox)
from PyQt5.QtGui import QStandardItem
import glob

import config
from models.recipe import Recipe
from support import gui_helpers
from recipe_category import RecipeCategory
from gui.base_gui_model import BaseGuiModel
from gui.meal_plan_gui_model import MealPlanGuiModel
from gui.emg_base import EMGTreeView, EMGMessageBox
from support.filter_collection import FilterCollection


class RecipeListItem(QStandardItem):
    def __init__(self, recipe: Recipe):
        super().__init__()
        self.id = recipe.id
        self.setText(recipe.title)


class RecipeListGuiModel(BaseGuiModel):
    def __init__(self, parent):
        super().__init__(parent)
        self.active_recipes = FilterCollection()
        self.list_view = EMGTreeView()
        self.list_view.setRootIsDecorated(False)
        self.list_view.setAlternatingRowColors(True)

        self.new_recipe_button = gui_helpers.create_tool_button("New Recipe")
        self.new_recipe_button.setToolTip(config.get_tooltip("new_recipe_button"))
        self.save_recipe_button = gui_helpers.create_tool_button("Save Recipe")
        self.save_recipe_button.setToolTip(config.get_tooltip("save_recipe_button"))
        self.delete_recipe_button = gui_helpers.create_tool_button("Delete Recipe")
        self.delete_recipe_button.setToolTip(config.get_tooltip("delete_recipe_button"))
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.new_recipe_button)
        self.button_layout.addWidget(self.save_recipe_button)
        self.button_layout.addWidget(self.delete_recipe_button)
        self.new_recipe_button.clicked.connect(self.new_recipe)
        self.save_recipe_button.clicked.connect(self.save_recipe)
        self.delete_recipe_button.clicked.connect(self.delete_recipe)

        self.model = gui_helpers.create_treeview_model(self.parent, ["Name", "Category"])

        self.list_layout = QVBoxLayout()
        self.recipe_list_head_layout = QHBoxLayout()
        self.recipe_list_label = QLabel("Recipes")
        self.recipe_category_combo = QComboBox()
        self.recipe_category_combo.addItem("--  Category  --")
        self.recipe_category_combo.addItems([category.value for category in RecipeCategory])
        self.recipe_category_combo.currentTextChanged.connect(self.filter_by_category)
        self.recipe_list_head_layout.addWidget(self.recipe_list_label)
        self.recipe_list_head_layout.addWidget(self.recipe_category_combo)

        self.list_layout.addLayout(self.recipe_list_head_layout)
        self.list_layout.addWidget(self.list_view)
        self.list_layout.addLayout(self.button_layout)
        self.group_box.setLayout(self.list_layout)
        self.group_box.setMaximumWidth(350)

        self.list_view.setModel(self.model)
        self.list_view.resizeColumnToContents(1)
        self.list_view.clicked.connect(self.parent.load_active_recipe)

    def delete_recipe(self):
        if EMGMessageBox.confirm(
                self.parent,
                "Delete recipe?",
                "Are you sure you want to delete this recipe?"
        ):
            try:
                self.model.removeRow(self.parent.current_idx.row())
            except FileNotFoundError as e:
                EMGMessageBox.info(
                    self.parent,
                    "Error",
                    "Could not delete recipe:\n\n" + str(e)
                )

    def save_recipe(self):
        self.get_selected_recipe().save()
        print("SAVED")

    def load_recipes(self):
        for path in glob.glob("resources/recipes/*.json"):
            with open(path, "r") as file:
                recipe = Recipe()
                recipe.from_json(file.read())
                recipe.file = path
                self.recipes.append(recipe)
                self.active_recipes.append(recipe)
                print("Loading recipe - ", [recipe.title, recipe.image])
        self.parent.refresh()

    def filter_by_category(self):
        self.active_recipes = FilterCollection()
        try:
            recipe_category = RecipeCategory(self.recipe_category_combo.currentText())

            if recipe_category not in RecipeCategory or recipe_category == RecipeCategory.DEFAULT:
                self.active_recipes.extend([recipe for recipe in self.recipes])
            else:
                for recipe in self.recipes:
                    if recipe.primary_category == recipe_category:
                        self.active_recipes.append(recipe)
        except:
            print("Error in selecting recipe category")
            self.active_recipes.extend([recipe for recipe in self.recipes])

        self.refresh()

    def add_recipe_to_table(self, recipe: Recipe):
        self.model.appendRow(RecipeListItem(recipe))
        # self.model.setData(self.model.index(0, 0), title)
        self.model.setData(self.model.index(self.model.rowCount() - 1, 1), recipe.primary_category.value)

    def new_recipe(self):
        recipe = Recipe()
        recipe.title = config.DEFAULT_RECIPE_TITLE
        recipe.id = self.recipes.max("id") + 1
        recipe.primary_category = RecipeCategory.DEFAULT
        self.recipes.insert(0, recipe)
        self.model.insertRow(0, RecipeListItem(recipe))
        self.model.setData(self.model.index(0, 0), recipe.title)
        self.model.setData(self.model.index(0, 1), recipe.primary_category.value)

        try:
            self.parent.current_idx = self.list_view.selectedIndexes()[0]
        except IndexError:
            pass

    def clear_listview_rows(self):
        self.model.removeRows(0, self.model.rowCount())

    def refresh(self):
        self.clear_listview_rows()
        for recipe in self.active_recipes:
            self.add_recipe_to_table(recipe)

    def get_selected_recipe(self):
        selected_indices = self.list_view.selectedIndexes()
        self.parent.current_idx = selected_indices[0]
        item = self.model.itemFromIndex(self.parent.current_idx)
        recipe = self.recipes.where("id", item.id).first()
        self.state.active_recipe = recipe

        return recipe
