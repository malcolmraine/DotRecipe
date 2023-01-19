# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from typing import Any

from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QListView,
    QListWidget,
)

import config
from gui.base_gui_model import BaseGuiModel
from gui.base_gui_model import GuiState
from models.recipe_instruction import RecipeInstruction
from support import gui_helpers
from support.filter_collection import FilterCollection


class InstructionItemModel(QStandardItemModel):
    def __init__(self, parent, headers, state: GuiState):
        super().__init__(0, len(headers), parent)
        self.state = state
        self.number_rgx = re.compile(r"[0-9]+\.\s*(.*)")

        for idx, header in enumerate(headers):
            self.setHeaderData(idx, Qt.Horizontal, header)

    def setData(self, index: QModelIndex, value: Any, role: int = Qt.EditRole) -> bool:
        # print("Updating instructions: ", value, index.row(), index.column())
        recipe = self.state.active_recipe
        instruction = recipe.instructions[index.row()]

        if str(value)[0].isnumeric():
            parts = self.number_rgx.findall(str(value))
            if len(parts) > 0:
                instruction.text = parts[0]
            else:
                instruction.text = str(value)
        else:
            instruction.text = str(value)

        return super(InstructionItemModel, self).setData(
            index, f"{index.row() + 1}.  {instruction.text}", role
        )


class InstructionsGuiModel(BaseGuiModel):
    def __init__(self, parent):
        super().__init__(parent)
        self.list_layout = QVBoxLayout()
        self.label = QLabel("Instructions")
        upper_layout = QHBoxLayout()
        label_layout = QHBoxLayout()
        label_layout.setAlignment(Qt.AlignLeft)
        label_layout.addWidget(self.label)
        upper_layout.addLayout(label_layout)
        self.list_view = self.make_listview()

        self.list_layout.addWidget(self.label)
        self.list_layout.addWidget(self.list_view)
        self.add_btn = gui_helpers.create_tool_button("Add")
        self.add_btn.clicked.connect(self.add_instruction)
        self.add_btn.setToolTip(config.get_tooltip("add_instruction_button"))
        self.remove_btn = gui_helpers.create_tool_button("Remove")
        self.remove_btn.clicked.connect(self.remove_instruction)
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
        self.group_box.setMaximumWidth(600)
        self.set_model(InstructionItemModel(self.parent, [""], self.state))
        # self.set_model(QStandardItemModel(0, 1, self.parent))

    def clear_listview_rows(self):
        if self.model is not None:
            self.model.removeRows(0, self.model.rowCount())

    def set_model(self, model):
        self.model = model
        self.list_view.setModel(self.model)

    def make_listview(self):
        list_view = QListView()
        list_view.setWordWrap(True)
        list_view.setSpacing(5)

        return list_view

    def make_listwidget(self):
        list_view = QListWidget()
        list_view.setWordWrap(True)
        list_view.setSpacing(5)

        return list_view

    def refresh(self):
        self.clear_listview_rows()
        for idx, instruction in enumerate(self.state.active_recipe.instructions):
            self.insert_row_at_end(instruction)

    def add_instruction(self):
        active_recipe = self.state.active_recipe

        if active_recipe:
            instruction = RecipeInstruction()
            self.state.active_recipe.instructions.append(instruction)
            self.insert_row_at_end(f"{self.model.rowCount() + 1}. {instruction.text}")

    def remove_instruction(self):
        selected_indexes = self.list_view.selectedIndexes()

        if len(selected_indexes):
            self.model.removeRow(selected_indexes[0].row())

    def get_as_list(self):
        items = FilterCollection()

        for row in range(self.model.rowCount()):
            index = self.model.index(row, 1)
            item = self.model.data(index, Qt.DisplayRole)
            items.append(item)
        return items
