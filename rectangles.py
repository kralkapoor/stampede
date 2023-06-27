from multiprocessing import Pool
from datetime import datetime
import os
from PIL import Image, ImageDraw
import time
from staticDicts import colours, rect_paths
from stamps import colour_sub
from initDirs import init_all

# OS variables
img_dir = os.listdir('./img')

# PIL variables
valid_formats = ('jpg', 'JPG', 'PNG', 'png')
quality_val = 100
now = datetime.now()

rect_files = (file for file in img_dir if file.endswith(valid_formats))

def pool_handler():
    if not rect_files:
        print('Nothing to process')
        return
    p = Pool()
    p.map(work_handler,rect_files)
    
def work_handler(file):
# Convert valid formats to png to allow RGBA
    start = time.time()
    no_extension = file[:file.index('.')+1]
    as_png = f'{no_extension}png'

    try:
        os.rename(f'img/{file}', f'img/{as_png}')
    except FileExistsError:
        with open('log.txt', 'a') as log:
            log.write(
                f'{now.strftime("%d/%m/%Y, %H:%M:%S")}: "{as_png}" ERROR! FILE ALREADY EXISTS\n')
        return
    try:
        image = Image.open(f'img/{as_png}')
        canvas = Image.new('RGBA', image.size, (255,255,255,255))
        ImageDraw.Draw(canvas)
        canvas.paste(image)

        # check for custom stamp to determine one or many colours
        custom_stamp = False
        try:
            custom_stamp = no_extension.count('&') == 1
        except ValueError:
            print(f'Processing {as_png} as generic stamp - all colours')
            
        path = ''    
        if custom_stamp:
            path = rect_paths['Custom']
            match no_extension[no_extension.index('&'):-1]:
                case '&R':
                    canvas = colour_sub(canvas, colours['R']) #red
                case '&G':
                    canvas = colour_sub(canvas, colours['G']) #medium sea green
                case '&B':
                    canvas = colour_sub(canvas, colours['B']) #cornflour blue
                case '&P':
                    canvas = colour_sub(canvas, colours['P']) #hot pink
                case '&PP':
                    canvas = colour_sub(canvas, colours['PP']) #dark violet
                case _:
                    canvas = colour_sub(canvas, colours['Black']) #default to black if not specified
                    
            canvas.save(f'img/Processed/Rectangles/{path}/{as_png}',quality=100)
            
            # Write to log
            append_to_log(start, time.time(),as_png,'log.txt')

        # If it's not a custom stamp, then create a copy in each standard colour    
        else:
            for code, colour_value in colours.items():
                rect_img = colour_sub(canvas.copy(), colour_value)
                rect_img.save(f'img/Processed/Rectangles/{rect_paths[code]}/{no_extension[:-1]}&{code}.png',quality=quality_val)
                
            append_to_log(start,time.time(),as_png,'log.txt')
        # Archive 
        os.replace(f'img/{as_png}',f'img/zArchive/{as_png}')
        
    except Exception as e:
        with open('log.txt', 'a') as log:
                log.write(
                    f'{now.strftime("%d/%m/%Y %H:%M")}: UNEXPECTED ERROR PROCESSING {as_png}\n')
                log.write(f'    Reason: {e}\n')

def append_to_log(start_time : float, end_time : float, img_file, log_file: str) -> None:
    with open(f'{log_file}', 'a') as log:
                log.write(
                    f'{now.strftime("%d/%m/%Y %H:%M")}: rect {img_file} processed in {round(end_time-start_time,2)}s\n')
    
if __name__ == '__main__':
    init_all()
    pool_handler()