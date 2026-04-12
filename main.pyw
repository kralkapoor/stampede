"""Stampede Resizer — main entry point."""

import os
import sys

from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow
from settings.logging_config import setup_logging


def main():
    # When running as a frozen exe, set CWD to the exe's directory so that
    # relative paths (img/, stampede.log, etc.) resolve next to the executable.
    if getattr(sys, "frozen", False):
        os.chdir(os.path.dirname(sys.executable))

    setup_logging()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
