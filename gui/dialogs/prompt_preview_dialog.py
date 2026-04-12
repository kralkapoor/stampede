"""Prompt dialog with image preview for avatar editing.

Shows the user what image they're about to edit alongside a prompt field,
so they can write context-aware instructions. Separated from handler logic
so avatar_edit_handler doesn't need to know about any GUI framework.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QDialog, QHBoxLayout, QLabel, QPushButton,
                               QTextEdit, QVBoxLayout)


class PromptPreviewDialog(QDialog):
    """Dialog with image preview on the left and editable prompt on the right."""

    def __init__(self, parent, image_path: str, image_filename: str):
        super().__init__(parent)
        self.setWindowTitle("Edit Avatar - Modify Existing Image")
        self.resize(1200, 600)

        outer_layout = QVBoxLayout(self)

        content_layout = QHBoxLayout()

        # Left: image preview
        image_layout = QVBoxLayout()

        # QPixmap handles png/jpg/jpeg/webp natively
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(image_label)

        filename_label = QLabel(f"Editing: {image_filename}")
        filename_label.setStyleSheet("font-weight: bold; font-size: 10pt;")
        filename_label.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(filename_label)

        # Pin preview to the top so it doesn't float to the vertical centre
        # when the dialog is taller than the image
        image_layout.addStretch()
        content_layout.addLayout(image_layout)

        # Right: prompt — gets stretch priority so the text area fills
        # available space while the preview stays at its fixed 300px
        prompt_layout = QVBoxLayout()

        instruction_label = QLabel("Describe how you want to modify this image:")
        instruction_label.setStyleSheet("font-weight: bold; font-size: 12pt;")
        prompt_layout.addWidget(instruction_label)

        self._text_edit = QTextEdit()
        self._text_edit.setPlainText("Please modify this image by: ")
        prompt_layout.addWidget(self._text_edit)

        content_layout.addLayout(prompt_layout, stretch=1)
        outer_layout.addLayout(content_layout)

        # Bottom buttons
        button_layout = QHBoxLayout()

        cancel_button = QPushButton("Cancel")
        cancel_button.setFixedWidth(120)
        cancel_button.setStyleSheet("background-color: red; color: white; font-weight: bold; font-size: 10pt;")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        button_layout.addStretch()

        edit_button = QPushButton("Edit Image")
        edit_button.setFixedWidth(120)
        edit_button.setStyleSheet("background-color: green; color: white; font-weight: bold; font-size: 10pt;")
        edit_button.clicked.connect(self.accept)
        button_layout.addWidget(edit_button)

        outer_layout.addLayout(button_layout)

    def get_prompt(self) -> str:
        return self._text_edit.toPlainText()
