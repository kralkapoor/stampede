"""Main application window.

Acts as the Mediator between GUI dialogs and backend handlers. Handlers don't
know about the GUI, and dialogs don't know about handlers — MainWindow
coordinates between them so neither side carries the other's dependencies.
"""

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget

from gui.dialogs.processing_dialog import ProcessingDialog
from gui.dialogs.prompt_dialog import PromptDialog
from gui.dialogs.prompt_preview_dialog import PromptPreviewDialog
from handling.avatar_edit_handler import AvatarEditHandler
from handling.avatar_handler import AvatarHandler
from handling.imagehandler.circle_handler import CircleHandler
from handling.imagehandler.rectangle_handler import RectangleHandler


class MainWindow(QWidget):
    """Main application window with action buttons."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stampede Resizer")
        self.resize(550, 200)
        self.setStyleSheet("MainWindow { background-color: white; }")

        self._rectangle_handler = RectangleHandler()
        self._circle_handler = CircleHandler()
        self._avatar_handler = AvatarHandler()
        self._avatar_edit_handler = AvatarEditHandler()

        layout = QVBoxLayout(self)

        # Stampede Logo
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("assets/logo.png")
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap)
        layout.addWidget(logo_label)

        # Button row
        button_layout = QHBoxLayout()

        buttons = [
            ("Rectangles", "lightblue", self._on_rectangles),
            ("Circles", "pink", self._on_circles),
            ("New Avatar", "#ff3030", self._on_new_avatar),
            ("Edit Avatar", "orange", self._on_edit_avatar),
        ]

        for text, color, handler in buttons:
            btn = QPushButton(text)
            btn.setStyleSheet(f"background-color: {color}; border: none; padding: 5px 10px; color: black;")
            btn.clicked.connect(handler)
            button_layout.addWidget(btn)

        layout.addLayout(button_layout)

    def _run_with_processing_dialog(self, title: str, message: str, callback):
        """Shared by all buttons — wraps any handler call in a processing dialog.

        Keeps the pattern consistent: show progress, run in background, report result.
        Without this, each button handler would duplicate the dialog/messagebox logic.
        """
        dialog = ProcessingDialog(self, title, message, callback)
        if dialog.exec() == ProcessingDialog.Accepted:
            QMessageBox.information(self, "Success", "Processing completed successfully!")
        else:
            QMessageBox.critical(self, "Error", f"Error during processing: {dialog.error_message}")

    def _on_rectangles(self):
        self._run_with_processing_dialog("Processing...", "Processing rectangles...", self._rectangle_handler.execute)
        sys.exit(0)

    def _on_circles(self):
        self._run_with_processing_dialog("Processing...", "Processing circles...", self._circle_handler.execute)
        sys.exit(0)

    def _on_new_avatar(self):
        # Collect the prompt first. If the user cancels, we skip the API call entirely
        prompt_dialog = PromptDialog(self, self._avatar_handler.prompt)
        if prompt_dialog.exec() != PromptDialog.Accepted:
            return

        user_prompt = prompt_dialog.get_prompt()
        print(f"prompt = {user_prompt}")

        self._run_with_processing_dialog(
            "Processing...",
            "Generating avatar...",
            lambda: self._avatar_handler.process_avatar(user_prompt),
        )
        sys.exit(0)

    def _on_edit_avatar(self):
        # Validate before showing the preview dialog. Fail fast so the user
        # doesn't write a prompt only to find out there's no image to edit
        try:
            image_file = self._avatar_edit_handler.validate_single_image()
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        image_path = f"img/{image_file}"
        preview_dialog = PromptPreviewDialog(self, image_path, image_file)
        if preview_dialog.exec() != PromptPreviewDialog.Accepted:
            return

        user_prompt = preview_dialog.get_prompt()
        print(f"edit prompt = {user_prompt}")

        self._run_with_processing_dialog(
            "Processing...",
            "Processing image...",
            lambda: self._avatar_edit_handler.process_edit_avatar(user_prompt, image_file),
        )
        sys.exit(0)
