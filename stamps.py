from multiprocessing import Pool
from datetime import datetime
import os
from PIL import Image, ImageDraw
import time
from staticDicts import colours
from initDirs import init_all

# OS variables
img_dir = os.listdir('./img')

# PIL variables
valid_formats = ('jpg', 'JPG', 'PNG', 'png')
quality_val = 100
curr_width = 0
curr_height = 0
curr_canvas_size = (0, 0)
now = datetime.now()
standard_size = (200,200)

# MP variables
# max_cores = multiprocessing.cpu_count()
# cores = 4
imgs_for_processing = (file for file in img_dir if file.endswith(valid_formats))

def colour_sub(image, colour: tuple):
    pixel_data = image.getdata()
    new_image = []

    for data in pixel_data:
        if data[3] != 0 and data[0] < 200:
            new_image.append(colour)
        else:
            new_image.append(data)

    image.putdata(new_image)
    return image

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

        image = Image.open(f'img/{as_png}')

        try:
            # set sizes and calculate max dimensions for canvas
            curr_width, curr_height = image.size
            max_dimension = max(curr_width + 100, curr_height + 100)
            curr_canvas_size = (max_dimension, max_dimension)

            # instantiate canvas and paste in image and a border circle
            canvas = Image.new('RGBA', curr_canvas_size, (255, 255, 255, 255))
            ImageDraw.Draw(canvas)
            canvas.paste(image, (50, 50))

            # crop image with circle
            cropped = canvas.crop(
                (20, 20, max_dimension - 20, max_dimension -20))

            # create transparent mask for the cropped image
            mask = Image.new('L', cropped.size)
            mask_draw = ImageDraw.Draw(mask)
            width, height = cropped.size
            mask_draw.ellipse((2.5, 2.5, width-5, height-5), fill=255)

            # add transparent background to mask
            cropped.putalpha(mask)
    
            # check for colour processing and sub if is_coloured is true
            is_coloured = False
            try:
                is_coloured = no_extension.count('&') == 1
            except ValueError:
                print(f'{file} colour not specified. Processing in B&W format')

            multi_colour : bool = False

            if is_coloured:
                match no_extension[no_extension.index('&'):-1]:
                    case '&R':
                        cropped = colour_sub(cropped, colours['R']) #red
                    case '&G':
                        cropped = colour_sub(cropped, colours['G']) #medium sea green
                    case '&B':
                        cropped = colour_sub(cropped, colours['B']) #cornflour blue
                    case '&P':
                        cropped = colour_sub(cropped, colours['P']) #hot pink
                    case '&PP':
                        cropped = colour_sub(cropped, colours['PP']) #dark violet
                    case '&E': #make a copy for all colours 
                        multi_colour = True
                        # Need to iterate over all key:value pairs in std colours
                        for code, colour in colours.items():
                            colour_cropped = colour_sub(cropped.copy(), colour)
                            colour_cropped = standardise_size(colour_cropped)
                            colour_as_png = f'{no_extension}{code}.png'
                            save_image(colour_cropped, colour_as_png)
                        archive_image(file)
            else:
                cropped = colour_sub(cropped, colours['Black']) #black (darken the grey pixels)

            if not multi_colour:
                # STANDARDISE THE SIZES OF STAMPS
                cropped = standardise_size(cropped)
                # Save image
                save_image(cropped, as_png)
                archive_image(as_png)

            # Write to log
            end = time.time()

            with open('log.txt', 'a') as log:
                log.write(
                    f'{now.strftime("%d/%m/%Y %H:%M")}: circle {as_png} processed in {round(end-start,2)}s\n')

        except Exception as e:
            with open('log.txt', 'a') as log:
                log.write(
                    f'{now.strftime("%d/%m/%Y %H:%M")}: UNEXPECTED ERROR PROCESSING {as_png}\n')
                log.write(f'    Reason: {e}\n')


def standardise_size(cropped_image):
    try:
        res = cropped_image.resize(standard_size)
        return res 
    except:
        print('exception on standardise_size')
    return

def save_image(image_to_save,file_name_with_extension):
    try:
        image_to_save.save(f'img/Processed/resized_{file_name_with_extension}', quality=quality_val)
    except Exception as e:
        print('exception on save_image')
    return
        
def archive_image(image_to_archive):
    os.replace(f'img/{image_to_archive}', f'img/zArchive/{image_to_archive}')

def pool_handler():
    # p = Pool(cores)
    p = Pool() #default processes = cpu_count()
    p.map(work_handler, imgs_for_processing)

if __name__ == '__main__':
    init_all()
    pool_handler()