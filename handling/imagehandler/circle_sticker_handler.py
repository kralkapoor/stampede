"""Circle sticker handler for cropping images into circular stickers."""

import os
import time

from PIL import Image, ImageDraw

from settings.static_dicts import PROCESSED_DIR_STICKER

from ..base_image_handler import BaseImageHandler


# new class for stickers
class CircleStickerHandler(BaseImageHandler):
    """Crops images maintaining aspect ratio for circular stickers."""

    def pool_handler(self):
        super().pool_handler()
        self._open_save_destination(PROCESSED_DIR_STICKER)

    def _save_image(self, image_to_save, file_name_with_extension):
        """Saves the image for stickers

        Args:
            image_to_save (Image): Image to save
            file_name_with_extension (str): New file name, with the filetype extension (e.g. png)
        """
        try:
            image_to_save.save(f"img/Processed/Stickers/resized_{file_name_with_extension}", quality=self.quality_val)
        except Exception:
            print("exception on save_image")

    def convert_image_to_rgb_with_background_colour(self, image, bg_colour: str):
        """Convert image to RGB with specified background color."""
        converted_image = Image.new("RGB", image.size, bg_colour)
        if image.mode == "RGBA":
            try:
                converted_image.paste(image, (0, 0), image)
            except Exception:
                self._append_ad_hoc_comment_to_log(f"bad transparency mask on {image}. bypassing...\n", self.log)
                print(f"WARNING: bad transparency mask on {image}. bypassing...")
                converted_image.paste(image, (0, 0))
        else:
            converted_image.paste(image, (0, 0))
        return converted_image

    # override super.work_handler
    def _work_handler(self, file):
        # Convert valid formats to png to allow RGBA
        start = time.time()
        no_extension = file[: file.index(".") + 1]
        path_as_png = f"{no_extension}png"

        rename_success = self._rename_file(file, path_as_png)
        if not rename_success:
            return

        # prep the image with a white background (sticker background must be white)
        # this accommodates when a png is provided which already has a transparent bg
        image = Image.open(f"img/{path_as_png}")
        image = self.convert_image_to_rgb_with_background_colour(image, "white")

        try:
            sticker_img = self.resize(image)
            self._append_processed_result_to_log(start, time.time(), path_as_png, self.log)
            self._save_image(sticker_img, path_as_png)
            self._archive_image(path_as_png)
        except Exception as e:
            self._append_ad_hoc_comment_to_log(
                f'{self.now.strftime("%d/%m/%Y %H:%M")}: UNEXPECTED ERROR PROCESSING {path_as_png}\n', self.log
            )
            self._append_ad_hoc_comment_to_log(f"    Reason: {e}\n", self.log)

    def paste_image_to_centre_of_canvas(self, desired_size, image_to_paste, curr_width, curr_height):
        """Paste image to center of canvas with proper alignment."""
        canvas = Image.new("RGBA", desired_size, (255, 255, 255, 255))
        ImageDraw.Draw(canvas)

        if curr_width > curr_height:
            difference = curr_width - curr_height
            canvas.paste(image_to_paste, (0, round(difference / 2)))
        elif curr_height > curr_width:
            difference = curr_height - curr_width
            canvas.paste(image_to_paste, (round(difference / 2), 0))
        else:
            canvas.paste(image_to_paste, (0, 0))

        return canvas

    def create_transparent_mask(self, canvas_size, img_dimension_max):
        """Create circular transparent mask for stickers."""
        mask = Image.new("L", canvas_size)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, img_dimension_max, img_dimension_max), fill=255)
        return mask

    def resize(self, image):
        """Resize image maintaining aspect ratio for circular stickers."""
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
