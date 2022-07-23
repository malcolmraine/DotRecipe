# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import (Qt)
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (QGroupBox, QHBoxLayout, QLabel, QVBoxLayout,
                             QListView, QListWidget)

import config
from support import gui_helpers
from gui_models.base_gui_model import BaseGuiModel
from gui_models.prints_and_exports import PrintsAndExports


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
        self.list_view.chang

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
        self.set_model(QStandardItemModel(0, 1, self.parent))

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
        print("Active recipe: ")
        for idx, instruction in enumerate(self.state.active_recipe.instructions):
            self.insert_row_at_end(f"{idx + 1}.  \0{instruction}")

    def add_instruction(self):
        self.insert_row_at_end(f"{self.model.rowCount() + 1}. \0")

    def remove_instruction(self):
        selected_indexes = self.list_view.selectedIndexes()

        if len(selected_indexes):
            self.model.removeRow(selected_indexes[0].row())

    def get_as_list(self):
        items = []

        for row in range(self.model.rowCount()):
            index = self.model.index(row, 1)
            item = self.model.data(index, Qt.DisplayRole)
            items.append(item)
        return items


