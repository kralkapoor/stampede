from ImageProcessing.ImageProcessor import ImageHandler
import time
import os
from PIL import Image, ImageDraw
from settings.staticDicts import colours, circle_dir_on_process

class Circles(ImageHandler):

    def __init__(self):
        super().__init__()

    def _save_image(self, image_to_save, file_name_with_extension):
        """Saves the image for circle processing into a Circles subfolder

        Args:
            image_to_save (Image): Image to save
            file_name_with_extension (str): New file name, with the filetype extension (e.g. png)
        """
        try:
            image_to_save.save(f'img/Processed/Circles/resized_{file_name_with_extension}', quality=self.quality_val)
            if os.name == 'nt':
                abs_path = os.path.realpath(circle_dir_on_process)
                os.startfile(abs_path)
        except Exception as e:
            print('exception on save_image')
        return

    def _standardise_size(self, cropped_image):
        """Resize the given image to the configured standard size

        Args:
            cropped_image (Image): Image to crop

        Returns:
            Either the newly cropped image or nothing on exception
        """
        
        # if the cfg size is not specified, just take the smallest dimension for best resolution
        if self.standard_size == None:
            self.standard_size = (min(cropped_image.size),min(cropped_image.size))
        
        try:
            res = cropped_image.resize(self.standard_size)
            return res
        except:
            print('exception on standardise_size')
        return

    # Override super.work_handler
    def work_handler(self, file):
        # Convert valid formats to png to allow RGBA
        start = time.time()
        no_extension = file[:file.index('.') + 1]
        as_png = f'{no_extension}png'

        try:
            os.rename(f'img/{file}', f'img/{as_png}')
        except FileExistsError:
            with open(self.log, 'a') as log:
                log.write(
                    f'{self.now.strftime("%d/%m/%Y, %H:%M:%S")}: "{as_png}" ERROR! FILE ALREADY EXISTS\n')
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
                (20, 20, max_dimension - 20, max_dimension - 20))

            # create transparent mask for the cropped image
            mask = Image.new('L', cropped.size)
            mask_draw = ImageDraw.Draw(mask)
            width, height = cropped.size
            mask_draw.ellipse((2.5, 2.5, width - 5, height - 5), fill=255)

            # add transparent background to mask
            cropped.putalpha(mask)

            # check for colour processing and sub if is_coloured is true
            is_coloured = False
            try:
                is_coloured = no_extension.count('&') == 1
            except ValueError:
                print(f'{file} colour not specified. Processing in B&W format')

            multi_colour: bool = False

            if is_coloured:
                match no_extension[no_extension.index('&'):-1]:
                    case '&R':
                        cropped = self.colour_sub(cropped, colours['R'])  # red
                    case '&G':
                        cropped = self.colour_sub(cropped, colours['G'])  # medium sea green
                    case '&B':
                        cropped = self.colour_sub(cropped, colours['B'])  # cornflour blue
                    case '&P':
                        cropped = self.colour_sub(cropped, colours['P'])  # hot pink
                    case '&PP':
                        cropped = self.colour_sub(cropped, colours['PP'])  # dark violet
                    case '&E':  # make a copy for all colours
                        multi_colour = True
                        # Need to iterate over all key:value pairs in std colours
                        for code, colour in colours.items():
                            colour_cropped = self.colour_sub(cropped.copy(), colour)
                            colour_cropped = self._standardise_size(colour_cropped)
                            colour_as_png = f'{no_extension}{code}.png'
                            self._save_image(colour_cropped, colour_as_png)
                        self.archive_image(as_png)
            else:
                cropped = self.colour_sub(cropped, colours['Black'])  # black (darken the grey pixels)

            if not multi_colour:
                # STANDARDISE THE SIZES OF STAMPS
                cropped = self._standardise_size(cropped)
                # Save image
                self._save_image(cropped, as_png)
                self.archive_image(as_png)

            # Write to log
            end = time.time()
            self.append_to_log(start, time.time(), as_png, self.log)

        except Exception as e:
            with open(self.log, 'a') as log:
                log.write(
                    f'{self.now.strftime("%d/%m/%Y %H:%M")}: UNEXPECTED ERROR PROCESSING {as_png}\n')
                log.write(f'    Reason: {e}\n')
