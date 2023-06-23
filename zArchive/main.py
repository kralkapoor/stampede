from PIL import Image, ImageDraw
from datetime import datetime
import os
import time

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

def main():
    valid_formats = ('jpg', 'JPG', 'PNG', 'png')
    quality_val = 100
    curr_width = 0
    curr_height = 0
    curr_canvas_size = (0, 0)
    now = datetime.now()

    img_dir = os.listdir('./img')
    generator = (file for file in img_dir if file.endswith(valid_formats))

    for file in generator:

        # Convert valid formats to png to allow RGBA
        no_extension = file[:file.index('.')+1]
        as_png = f'{no_extension}png'
        os.rename(f'img/{file}', f'img/{as_png}')

        image = Image.open(f'img/{as_png}')

        try:
            # set sizes and calculate max dimensions for canvas
            curr_width, curr_height = image.size
            max_dimension = max(curr_width + 100, curr_height + 100)
            curr_canvas_size = (max_dimension, max_dimension)

            # instantiate canvas and paste in image and a border circle
            # canvas = Image.new('RGBA', curr_canvas_size, (255,255,255,0))
            canvas = Image.new('RGB', curr_canvas_size, (255, 255, 255))
            draw = ImageDraw.Draw(canvas)
            canvas.paste(image, (50, 50))
            # draw.ellipse((20, 20, max_dimension - 20, max_dimension - 20), outline='black', width=1)

            # crop image with circle
            cropped = canvas.crop(
                (20, 20, max_dimension - 20, max_dimension-20))

            # create empty background with circle
            mask = Image.new('L', cropped.size)
            mask_draw = ImageDraw.Draw(mask)
            width, height = cropped.size
            mask_draw.ellipse((2.5, 2.5, width-5, height-5), fill=255)

            # add transparent background to mask
            cropped.putalpha(mask)
    
            # check for colour processing and sub if is_coloured is true
            is_coloured = False
            try:
                # is_coloured = no_extension.index('&') != -1
                is_coloured = no_extension.count('&') == 1
                # print(no_extension[no_extension.index('&'):-1])
            except ValueError:
                print(f'{file} in B&W format')

            if is_coloured:
                match no_extension[no_extension.index('&'):-1]:
                    case '&R':
                        cropped = colour_sub(cropped, (255, 0, 0, 255)) #red
                    case '&G':
                        cropped = colour_sub(cropped, (60, 179, 113, 255)) #medium sea green
                    case '&B':
                        cropped = colour_sub(cropped, (100, 149, 237, 255)) #cornflour blue
                    case '&P':
                        cropped = colour_sub(cropped, (255, 105, 180, 255)) #hot pink
                    case '&PP':
                        cropped = colour_sub(cropped, (148, 0, 211, 255)) #dark violet

            cropped.save(
                f'img/processed/resized_{as_png}', quality=quality_val)
            os.replace(f'img/{as_png}', f'img/archive/{as_png}')

            with open('log.txt', 'a') as log:
                log.write(
                    f'{now.strftime("%d/%m/%Y, %H:%M:%S")}: "{as_png}" PROCESSED SUCCESSFULLY\n')
        except Exception as e:
            with open('log.txt', 'a') as log:
                log.write(
                    f'{now.strftime("%d/%m/%Y, %H:%M:%S")}: "{as_png}" ERROR\n')
                log.write(f'    {e}\n')


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(end - start)