import os
from settings.static_dicts import rect_paths

DIRS = (
            'img/',
            'img/Processed',
            'img/zArchive',
            'img/Processed/Rectangles',
            'img/Processed/Circles',
            'img/Processed/Stickers',
            'img/Processed/Avatars',
            'img/Processed/Avatars/Exemplars'
        )

def init_base_dirs():
    for dir in DIRS:
        try:
            os.mkdir(dir)
            print(f'Created dir for {dir}')
        except FileExistsError:
            pass

def init_rect_dirs():
    rect_dirs = [f'img/Processed/Rectangles/{rect_paths[key]}' for key in rect_paths]
    for dir in rect_dirs:
        try:
            os.mkdir(dir)
            print(f'Created dir for {dir}')
        except FileExistsError:
            pass

def init_all():
    init_base_dirs()
    init_rect_dirs()
    
if __name__ == '__main__':
    # relative pathing issue, so this should only be run from the GUI
    pass