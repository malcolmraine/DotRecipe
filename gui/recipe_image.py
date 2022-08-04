# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel
from PIL import Image
import random
from support import path_helpers
import config
from PyQt5.QtCore import Qt


class RecipeImage(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setText(args[0])
        self._text = None
        self.setAcceptDrops(True)
        self.setPixmap(QPixmap(self.text()))
        self.image_save_name = self.text()
        self.setToolTip(config.get_tooltip("default_image"))
        self.setAlignment(Qt.AlignCenter)

    def dragEnterEvent(self, e):
        if e.mimeData().hasImage():
            self.setPixmap(QPixmap.fromImage(QImage(e.mimeData().imageData())))
        elif e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.add_item(e.mimeData().text())

    def add_item(self, text):
        if self.is_file_allowed(text):
            self.setPixmap(QPixmap(self.resize_image(text)))

    def resize_image(self, path: str):
        path = path_helpers.convert_unc(path)
        img = Image.open(path)
        resized = img.resize((480, 320))
        save_path = self.image_save_name
        resized.save(save_path)

        return save_path

    def setPixmap(self, pixmap):
        if pixmap.isNull():
            self._text = None
        else:
            self._text = self.text()
        super().setPixmap(pixmap)

    def text(self):
        if self._text:
            return self._text
        return super().text()

    @staticmethod
    def is_file_allowed(path: str):
        return path_helpers.endswith_any(
            path,
            [
                "jpg",
                "jpeg",
                "png",
                "webp",
            ],
        )

    def reset(self):
        ...
