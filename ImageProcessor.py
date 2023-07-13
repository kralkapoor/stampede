from multiprocessing import Pool
from datetime import datetime
import time
import os
from PIL import Image, ImageDraw
from config.initDirs import init_all
from config.staticDicts import colours, rect_paths, valid_formats_cfg, image_quality_cfg, standard_img_size_cfg, \
    log_location, circle_dir_on_process, rectangle_dir_on_process, sticker_dir_on_process


class ImageProcessor:
    def __init__(self):
        init_all()  # init prerequisite directories that are gitignored
        self.valid_formats = valid_formats_cfg
        self.quality_val = image_quality_cfg
        self.standard_size = standard_img_size_cfg
        # Current values
        self.curr_width = 0
        self.curr_height = 0
        self.curr_canvas_size = (0, 0)
        self.now = datetime.now()
        self.img_dir = os.listdir('./img')
        self.log = log_location
        # self.max_cores = multiprocessing.cpu_count()

    def fetch_imgs(self):
        """
        Loops through the img directory to identify suitable images

        Returns:
            Generator: of all the images for processing
        """
        files = (file for file in self.img_dir if file.endswith(self.valid_formats))
        return files

    def pool_handler(self):
        """
        Performs the work for processing. Applies the work_handler method to each file in the images generator
        """
        imgs = self.fetch_imgs()
        p = Pool()  # default processes = cpu_count()
        p.map(self.work_handler, imgs)

    def work_handler(self, file):
        """Defines the work to be done by the pool handler. Requires an override from a child class

        Args:
            file (Image): Each image in the img generator
        """
        print("Requires override")
        return

    def append_to_log(self, start_time: float, end_time: float, img_file, log_file: str):
        """Append a message to the log saying whether the img was successfully processed or not

        Args:
            start_time (float): the time that the pool handler was executed
            end_time (float): the time the pool handler completed
            img_file (_type_): each image file in the img generator
            log_file (str): the name of the log in ./config
        """
        with open(f'{log_file}', 'a') as log:
            log.write(
                f'{self.now.strftime("%d/%m/%Y %H:%M")}: {img_file} processed in {round(end_time - start_time, 2)}s\n')

    def colour_sub(self, image, colour: tuple):
        """Method to replace pixels over a certain opacity with that of another specified colour

        Args:
            image (Image): The image to have it's pixels replaced
            colour (tuple): New colour as a tuple (R,G,B,Opacity)

        Returns:
            Image: Recoloured image
        """
        pixel_data = image.getdata()
        new_image = []

        for data in pixel_data:
            if data[3] != 0 and data[0] < 200:
                new_image.append(colour)
            else:
                new_image.append(data)

        image.putdata(new_image)
        return image

    def archive_image(self, image_to_archive):
        """Moves the image to the archive folder (currently hardcoded)

        Args:
            image_to_archive (Image): Image to archive
        """
        os.replace(f'img/{image_to_archive}', f'img/zArchive/{image_to_archive}')


class Circles(ImageProcessor):

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


class Rectangles(ImageProcessor):

    def __init__(self):
        super().__init__()
        self.rect_paths = rect_paths

    # Override super.work_handler for rectangles specifically 
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
        try:
            image = Image.open(f'img/{as_png}')
            canvas = Image.new('RGBA', image.size, (255, 255, 255, 255))
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
                path = self.rect_paths['Custom']
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

                canvas.save(f'img/Processed/Rectangles/{path}/{as_png}', quality=100)
                if os.name == 'nt':
                    abs_path = os.path.realpath(rectangle_dir_on_process)
                    os.startfile(abs_path)

                # Write to log
                self.append_to_log(start, time.time(), as_png, self.log)

            # If it's not a custom stamp, then create a copy in each standard colour    
            else:
                for code, colour_value in colours.items():
                    rect_img = self.colour_sub(canvas.copy(), colour_value)
                    rect_img.save(f'img/Processed/Rectangles/{self.rect_paths[code]}/{no_extension[:-1]}&{code}.png',
                                  quality=self.quality_val)

                self.append_to_log(start, time.time(), as_png, self.log)
            # Archive 
            # os.replace(f'img/{as_png}',f'img/zArchive/{as_png}')
            self.archive_image(as_png)

        except Exception as e:
            with open(self.log, 'a') as log:
                log.write(
                    f'{self.now.strftime("%d/%m/%Y %H:%M")}: UNEXPECTED ERROR PROCESSING {as_png}\n')
                log.write(f'    Reason: {e}\n')


# new class for stickers
class Stickers(ImageProcessor):

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


if __name__ == '__main__':
    pass
