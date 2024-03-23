from ImageProcessing.ImageProcessor import ImageHandler
import time
import os
from PIL import Image, ImageDraw
from settings.staticDicts import sticker_dir_on_process

# new class for stickers
class CircleStickers(ImageHandler):

    def __init__(self):
        super().__init__()
        
    def pool_handler(self):
        super().pool_handler()
        self.open_save_destination()
        return

    def _save_image(self, image_to_save, file_name_with_extension):
        """Saves the image for stickers

        Args:
            image_to_save (Image): Image to save
            file_name_with_extension (str): New file name, with the filetype extension (e.g. png)
        """
        try:
            image_to_save.save(f'img/Processed/Stickers/resized_{file_name_with_extension}', quality=self.quality_val)
        except Exception as e:
            print('exception on save_image')
        return
    
    def open_save_destination(self) -> None:
        if os.name == 'nt':
            abs_path = os.path.realpath(sticker_dir_on_process)
            try:
                os.startfile(abs_path)
            except Exception as e:
                print("something wrong with opening explorer on open save destination")  
        return  
    
    def rename_file(self, file, new_name):
        try:
            os.rename(f'img/{file}', f'img/{new_name}')
            return True
        except FileExistsError:
            self.append_ad_hoc_comment_to_log(f'{self.now.strftime("%d/%m/%Y, %H:%M:%S")}: "{new_name}" ERROR! FILE ALREADY EXISTS\n')
            return False
    
    def convert_image_to_RGB_with_specific_background_colour(self, image, colour_string : str):
        converted_image = Image.new("RGB", image.size, colour_string)
        if image.mode == "RGBA":
            try:
                converted_image.paste(image, (0,0), image)
            except:
                self.append_ad_hoc_comment_to_log(f'bad transparency mask on {image}. bypassing...\n',self.log)
                print(f'WARNING: bad transparency mask on {image}. bypassing...')
                converted_image.paste(image, (0,0))
        else:
            converted_image.paste(image,(0,0))
        return converted_image
    
    # override super.work_handler
    def work_handler(self, file):
        # Convert valid formats to png to allow RGBA
        start = time.time()
        no_extension = file[:file.index('.') + 1]
        path_as_png = f'{no_extension}png'
        
        rename_success = self.rename_file(file, path_as_png)
        if not rename_success:
            return
        
        # prep the image with a white background (sticker background must be white)
        # this accommodates when a png is provided which already has a transparent bg
        image = Image.open(f'img/{path_as_png}')
        image = self.convert_image_to_RGB_with_specific_background_colour(image, "white")
        
        try:
            sticker_img = self.resize(image)
            self.append_processed_result_to_log(start, time.time(), path_as_png, self.log)
            self._save_image(sticker_img, path_as_png)
            self.archive_image(path_as_png)    
        except Exception as e:
            self.append_ad_hoc_comment_to_log( f'{self.now.strftime("%d/%m/%Y %H:%M")}: UNEXPECTED ERROR PROCESSING {path_as_png}\n',self.log)
            self.append_ad_hoc_comment_to_log( f'    Reason: {e}\n',self.log)
            
    def paste_image_to_centre_of_canvas(self, desired_size, image_to_paste, curr_width, curr_height):
        canvas = Image.new('RGBA', desired_size, (255, 255, 255, 255))
        ImageDraw.Draw(canvas)

        if curr_width > curr_height:
            difference = curr_width - curr_height
            canvas.paste(image_to_paste, (0,round(difference/2)))
        elif curr_height > curr_width:
            difference = curr_height - curr_width
            canvas.paste(image_to_paste, (round(difference/2),0))
        else:
            canvas.paste(image_to_paste,(0,0))
            
        return canvas
    
    def create_transparent_mask(self, canvas_size, img_dimension_max):
        mask = Image.new('L', canvas_size)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, img_dimension_max, img_dimension_max), fill=255)
        return mask
                        
    def resize(self, image):
        # set sizes and calculate max dimensions for canvas
        curr_width, curr_height = image.size
        # the proportions of stickers are not necessarily square
        # take the max dimension and create a canvas so that it fits everything
        dimension_max = max(curr_width, curr_height)
        canvas_size = (dimension_max, dimension_max)
        
        # instantiate canvas and paste in image and a border circle
        canvas = self.paste_image_to_centre_of_canvas(canvas_size, image, curr_width, curr_height)
        # create transparent mask for the cropped image
        mask = self.create_transparent_mask(canvas.size, dimension_max)
        # add transparent background to mask
        canvas.putalpha(mask)

        return canvas