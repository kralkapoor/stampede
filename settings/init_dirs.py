"""Directory initialization utilities."""

import os

from settings.static_dicts import RECT_PATHS

DIRS = (
    "img/",
    "img/Processed",
    "img/zArchive",
    "img/Processed/Rectangles",
    "img/Processed/Circles",
    "img/Processed/Stickers",
    "img/Processed/Avatars",
    "img/Processed/Avatars/Exemplars",
)


def init_base_dirs():
    """Initialize base processing directories."""
    for directory in DIRS:
        try:
            os.mkdir(directory)
            print(f"Created dir for {directory}")
        except FileExistsError:
            pass


def init_rect_dirs():
    """Initialize rectangle-specific directories."""
    rect_dirs = [f"img/Processed/Rectangles/{path}" for path in RECT_PATHS.values()]
    for directory in rect_dirs:
        try:
            os.mkdir(directory)
            print(f"Created dir for {directory}")
        except FileExistsError:
            pass


def init_all():
    """Initialize all required directories."""
    init_base_dirs()
    init_rect_dirs()


if __name__ == "__main__":
    # relative pathing issue, so this should only be run from the GUI
    pass
