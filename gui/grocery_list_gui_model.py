from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QTreeView,
)

import config
from gui.base_gui_model import BaseGuiModel
from gui.bubble_notification import ToastNotification
from support import gui_helpers


class GroceryListGuiModel(BaseGuiModel):
    def __init__(self, parent):
        super().__init__(parent)
        self.model = gui_helpers.create_treeview_model(
            self.parent, ["Qty", "Item", "Notes"]
        )
        self.list_layout = QVBoxLayout()
        self.list_view = QTreeView()

        self.list_layout.addWidget(self.list_view)
        self.list_view.setAlternatingRowColors(True)
        self.list_view.setModel(self.model)

        self.add_btn = gui_helpers.create_tool_button("Add")
        # TODO: connect add grocery list item button
        self.add_btn.setToolTip(config.get_tooltip("add_instruction_button"))
        self.remove_btn = gui_helpers.create_tool_button("Remove")
        self.save_btn = gui_helpers.create_tool_button("Save")
        self.save_btn.clicked.connect(self.save)
        # TODO: connect remove grocery list item button
        self.remove_btn.setToolTip(config.get_tooltip("remove_instruction_button"))
        self.add_remove_btn_layout = QHBoxLayout()
        self.add_remove_btn_layout.setAlignment(Qt.AlignLeft)
        self.add_remove_btn_layout.addWidget(self.save_btn)
        self.add_remove_btn_layout.addWidget(self.add_btn)
        self.add_remove_btn_layout.addWidget(self.remove_btn)
        self.button_layout = QHBoxLayout()
        self.button_layout.addLayout(self.add_remove_btn_layout)
        self.button_layout.addLayout(self.print_export_button_layout)
        self.list_layout.addLayout(self.button_layout)

        self.group_box.setLayout(self.list_layout)
        self.group_box.setMaximumWidth(1000)
        self.state.grocery_list.from_file("resources/grocery_list.json")
        self.refresh()

    def save(self):
        self.state.grocery_list.save()
        ToastNotification.show("Grocery list saved")

    def refresh(self):
        self.clear_listview_rows()
        for item in self.state.grocery_list.items:
            self.insert_row_at_end([f"{item.qty}", f"{item.name}", ""])

    def clear_listview_rows(self):
        self.model.removeRows(0, self.model.rowCount())
