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
    for directory in DIRS:
        try:
            os.mkdir(directory)
            print(f"Created dir for {directory}")
        except FileExistsError:
            pass


def init_rect_dirs():
    rect_dirs = [f"img/Processed/Rectangles/{RECT_PATHS[key]}" for key in RECT_PATHS]
    for directory in rect_dirs:
        try:
            os.mkdir(directory)
            print(f"Created dir for {directory}")
        except FileExistsError:
            pass


def init_all():
    init_base_dirs()
    init_rect_dirs()


if __name__ == "__main__":
    # relative pathing issue, so this should only be run from the GUI
    pass
