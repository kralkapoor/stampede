"""Stampede Resizer — main entry point."""

import sys
from multiprocessing import freeze_support

from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    # On Windows, multiprocessing.Pool (used in BaseImageHandler) spawns child
    # processes by re-executing the exe. freeze_support() tells those children
    # to act as workers instead of re-running main(), preventing infinite process
    # spawning. No-op when running from source.
    freeze_support()
    main()
