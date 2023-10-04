from ImageProcessing import ImageProcessor
import time
import os
from PIL import Image, ImageDraw
from config.staticDicts import colours, circle_dir_on_process, sticker_dir_on_process

# new class for stickers
class CircleStickers(ImageProcessor):

    def __init__(self):
        super().__init__()

    def _save_image(self, image_to_save, file_name_with_extension):
        """Saves the image for stickers

        Args:
            image_to_save (Image): Image to save
            file_name_with_extension (str): New file name, with the filetype extension (e.g. png)
        """
        try:
            image_to_save.save(f'img/Processed/Stickers/resized_{file_name_with_extension}', quality=self.quality_val)
            if os.name == 'nt':
                abs_path = os.path.realpath(sticker_dir_on_process)
                os.startfile(abs_path)
        except Exception as e:
            print('exception on save_image')
        return

    # override super.work_handler
    def work_handler(self, file):
        # Convert valid formats to png to allow RGBA
        start = time.time()
        no_extension = file[:file.index('.') + 1]
        as_png = f'{no_extension}png'

        try:
            os.rename(f'img/{file}', f'img/{as_png}')
        except FileExistsError:
            with open('log.txt', 'a') as log:
                log.write(
                    f'{self.now.strftime("%d/%m/%Y, %H:%M:%S")}: "{as_png}" ERROR! FILE ALREADY EXISTS\n')
            return

        image = Image.open(f'img/{as_png}')

        try:
            # set sizes and calculate max dimensions for canvas
            curr_width, curr_height = image.size

            # Calculate the min and max of width and height. 
            # The max of the two minus min can be used as a center square
            dimension_min = min(curr_width, curr_height)
            dimension_max = max(curr_width, curr_height)
            dimension_range = dimension_max - dimension_min

            curr_canvas_size = (dimension_min, dimension_min)

            # instantiate canvas and paste in image and a border circle
            canvas = Image.new('RGBA', curr_canvas_size, (255, 255, 255, 255))
            ImageDraw.Draw(canvas)

            # paste image and center in the square canvas bounds
            canvas.paste(image, (round(-dimension_range / 2), 0))

            # create transparent mask for the cropped image
            # width and height should be equal
            mask = Image.new('L', canvas.size)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0, dimension_min, dimension_min), fill=255)

            # add transparent background to mask
            canvas.putalpha(mask)
            # check for colour processing and sub if is_coloured is true
            is_coloured = False
            try:
                is_coloured = no_extension.count('&') == 1
            except ValueError:
                print(f'{file} in B&W format')

            if is_coloured:
                match no_extension[no_extension.index('&'):-1]:
                    case '&R':
                        canvas = self.colour_sub(canvas, colours['R'])  # red
                    case '&G':
                        canvas = self.colour_sub(canvas, colours['G'])  # medium sea green
                    case '&B':
                        canvas = self.colour_sub(canvas, colours['B'])  # cornflour blue
                    case '&P':
                        canvas = self.colour_sub(canvas, colours['P'])  # hot pink
                    case '&PP':
                        canvas = self.colour_sub(canvas, colours['PP'])  # dark violet
                    case _:
                        canvas = self.colour_sub(canvas, colours['Black'])  # default to black if not specified

            self._save_image(canvas, as_png)
            if os.name == 'nt':
                abs_path = os.path.realpath(circle_dir_on_process)
                os.startfile(abs_path)

            self.archive_image(as_png)
            self.append_to_log(start, time.time(), as_png, self.log)

        except Exception as e:
            with open('log.txt', 'a') as log:
                log.write(
                    f'{self.now.strftime("%d/%m/%Y %H:%M")}: UNEXPECTED ERROR PROCESSING {as_png}\n')
                log.write(f'    Reason: {e}\n')