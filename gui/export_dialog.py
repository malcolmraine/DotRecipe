from PyQt5.QtCore import (
    Qt,
)
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QComboBox,
)

from gui.bubble_notification import ToastNotification
from support import gui_helpers


class ExportDialog(QDialog):
    def __init__(self, parent, state):
        super().__init__(parent)
        self.state = state
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.export_combo = QComboBox()
        self.export_combo.addItems(
            [
                "HTML",
                "PDF",
                # "Microsoft To-Do",
            ]
        )
        main_layout.addWidget(self.export_combo)
        self.export_btn = gui_helpers.create_tool_button("Export")
        self.export_btn.clicked.connect(self.export)
        self.cancel_btn = gui_helpers.create_tool_button("Cancel")
        self.cancel_btn.clicked.connect(self.cancel)
        self.export_cancel_layout = QHBoxLayout()
        self.export_cancel_layout.addWidget(self.export_btn)
        self.export_cancel_layout.addWidget(self.cancel_btn)
        self.export_cancel_layout.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        main_layout.addLayout(self.export_cancel_layout)
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)

    def export(self):
        print("Export")
        if self.state is not None:
            ToastNotification.show(f"Exported {self.state.active_recipe.title}")
        self.close()

    def cancel(self):
        print("Cancel")
        self.close()

    def refresh(self):
        pass
