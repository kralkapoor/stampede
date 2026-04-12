"""Prompt editing dialog for avatar generation.

Encapsulates the "get a prompt from the user" interaction as a self-contained
dialog (Command pattern). The caller creates it, calls exec(), and inspects
the result — keeping prompt collection separate from avatar processing logic.
"""

from PySide6.QtWidgets import QDialog, QHBoxLayout, QPushButton, QTextEdit, QVBoxLayout


class PromptDialog(QDialog):
    """Dialog with an editable text area for the avatar generation prompt."""

    def __init__(self, parent, initial_prompt: str, title: str = "Avatar Processing Instructions"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(1000, 400)

        layout = QVBoxLayout(self)

        # Pre-filled so the user can tweak the default rather than writing from scratch
        self._text_edit = QTextEdit()
        self._text_edit.setPlainText(initial_prompt)
        self._text_edit.setTextColor("black")
        layout.addWidget(self._text_edit)

        # Button row
        button_layout = QHBoxLayout()

        cancel_button = QPushButton("Cancel")
        cancel_button.setFixedWidth(80)
        cancel_button.setStyleSheet("background-color: red; color: white;")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        button_layout.addStretch()

        ok_button = QPushButton("OK")
        ok_button.setFixedWidth(80)
        ok_button.setStyleSheet("background-color: green; color: white;")
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)

        layout.addLayout(button_layout)

    def get_prompt(self) -> str:
        """Exposes the user's input so the caller doesn't need to know about internal widgets."""
        return self._text_edit.toPlainText()
