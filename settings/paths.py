"""Path resolution utilities for frozen (PyInstaller) and dev environments."""

import os
import sys


def resource_path(relative_path: str) -> str:
    """Resolve path to a bundled read-only resource (e.g. assets/ image files).

    When frozen by PyInstaller, bundled files live under sys._MEIPASS.
    In development, they live relative to the project root (CWD).
    """
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS
    else:
        base = os.path.abspath(".")
    return os.path.join(base, relative_path)
