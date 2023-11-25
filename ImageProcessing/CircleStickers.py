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
    
    # override super.work_handler
    def work_handler(self, file):
        # Convert valid formats to png to allow RGBA
        start = time.time()
        no_extension = file[:file.index('.') + 1]
        as_png = f'{no_extension}png'
        
        rename_success = self.rename_file(file, as_png)
        if not rename_success:
            return

        image = Image.open(f'img/{as_png}')

        try:
            self.resize(image, as_png)
            self.append_processed_result_to_log(start, time.time(), as_png, self.log)    
        except Exception as e:
            self.append_ad_hoc_comment_to_log( f'{self.now.strftime("%d/%m/%Y %H:%M")}: UNEXPECTED ERROR PROCESSING {as_png}\n',self.log)
            self.append_ad_hoc_comment_to_log( f'    Reason: {e}\n',self.log)
                
    def resize(self, image, filename):
        # set sizes and calculate max dimensions for canvas
        curr_width, curr_height = image.size

        # the proportions of stickers are not necessarily square
        # take the max dimension and create a canvas so that it fits everything
        dimension_max = max(curr_width, curr_height)
        dimension_min = min(curr_width, curr_height)
        dimension_range = dimension_max - dimension_min
        
        curr_canvas_size = (dimension_max, dimension_max)

        # instantiate canvas and paste in image and a border circle
        canvas = Image.new('RGBA', curr_canvas_size, (255, 255, 255, 255))
        ImageDraw.Draw(canvas)


        print(curr_width, curr_height)
        
        if curr_width > curr_height:
            difference = curr_width - curr_height
            canvas.paste(image, (0,round(difference/2)))
        elif curr_height > curr_width:
            difference = curr_height - curr_width
            canvas.paste(image, (round(difference/2),0))
        

        # create transparent mask for the cropped image
        mask = Image.new('L', canvas.size)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, dimension_max, dimension_max), fill=255)

        # # add transparent background to mask
        canvas.putalpha(mask)

        self._save_image(canvas, filename)
        self.archive_image(filename)