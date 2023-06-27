import os
from staticDicts import rect_paths

def init_base_dirs():
    dirs = (f'img/',f'img/Processed',f'img/zArchive',f'img/Processed/Rectangles',f'img/Processed/Circles')
    for dir in dirs:
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

# def init_circle_dirs():
#     pass

def init_all():
    init_base_dirs()
    init_rect_dirs()
    
if __name__ == '__main__':
    init_all()