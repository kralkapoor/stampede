"""Stampede Resizer — main entry point."""

import os
import sys
from multiprocessing import freeze_support

from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow


def main():
    # When running as a frozen exe, set CWD to the exe's directory so that
    # relative paths (img/, log.txt, etc.) resolve next to the executable.
    if getattr(sys, "frozen", False):
        os.chdir(os.path.dirname(sys.executable))

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
