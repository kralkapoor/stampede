"""Circle handler for processing circular stamps with color themes."""

import os
import time

from PIL import Image, ImageDraw

from handling.base_image_handler import BaseImageHandler
from settings.static_dicts import COLOURS, PROCESSED_DIR_CIRCLE


class CircleHandler(BaseImageHandler):
    """Extends ImageHandler to specifically process circle shaped images used in the small, round stamp handles.

    Args:
        ImageHandlerBase (class): Base class from which to inherit save, logging, and multiprocessing functions.
    """

    def __init__(self):
        super().__init__()

    def pool_handler(self):
        super().pool_handler()
        self._open_save_destination(PROCESSED_DIR_CIRCLE)

    def _save_image(self, image_to_save, file_name_with_extension):
        """Saves the image for circle processing into a Circles subfolder

        Args:
            image_to_save (Image): Image to save
            file_name_with_extension (str): New file name, with the filetype extension (e.g. png)
        """
        try:
            image_to_save.save(f"img/Processed/Circles/resized_{file_name_with_extension}", quality=self.quality_val)
        except Exception:
            self._append_ad_hoc_comment_to_log(f"Exception on save_image for {file_name_with_extension}", self.log)

    def _standardise_size(self, cropped_image):
        """Resize the given image to the configured standard size

        Args:
            cropped_image (Image): Image to crop

        Returns:
            Either the newly cropped image or nothing on exception
        """

        # if the cfg size is not specified, just take the smallest dimension for best resolution
        if self.standard_size is None:
            self.standard_size = (min(cropped_image.size), min(cropped_image.size))

        try:
            res = cropped_image.resize(self.standard_size)
            return res
        except Exception:
            print("exception on standardise_size")
            return None

    # Override super.work_handler
    def _work_handler(self, file):
        # Convert valid formats to png to allow RGBA
        start = time.time()
        no_extension = file[: file.index(".") + 1]
        as_png = f"{no_extension}png"

        # rename the file and change extension to png so that we can apply transparent masks
        rename_success = self._rename_file(file, as_png)
        if not rename_success:
            return

        image = Image.open(f"img/{as_png}")

        try:
            cropped = self.resize(image)
            is_coloured: bool = self.check_is_coloured(no_extension)

            if is_coloured:
                colour_extension = self.determine_colour_extension(no_extension)
                # Convert the current picture into one of the standard colours
                final_image = self.recolour(cropped, no_extension, colour_extension)
                if final_image:
                    self._save_image(final_image, as_png)
            else:
                darkened_image = self.recolour_darken(cropped)
                self._save_image(darkened_image, f"{no_extension}png")
            self._archive_image(f"{no_extension}png")

            # Write to log
            self._append_processed_result_to_log(start, time.time(), as_png, self.log)

        except Exception as e:
            self._append_ad_hoc_comment_to_log(
                f'{self.now.strftime("%d/%m/%Y %H:%M")}: UNEXPECTED ERROR PROCESSING {as_png}\n', self.log
            )
            self._append_ad_hoc_comment_to_log(f"    Reason: {e}\n")

    def resize(self, image):
        """Resize image maintaining aspect ratio."""
        # set sizes and calculate max dimensions for canvas
        curr_width, curr_height = image.size
        max_dimension = max(curr_width + 100, curr_height + 100)
        curr_canvas_size = (max_dimension, max_dimension)

        # instantiate canvas and paste in image and a border circle
        canvas = Image.new("RGBA", curr_canvas_size, (255, 255, 255, 255))
        ImageDraw.Draw(canvas)
        canvas.paste(image, (50, 50))

        # crop image with circle
        cropped = canvas.crop((20, 20, max_dimension - 20, max_dimension - 20))

        # create transparent mask for the cropped image
        mask = Image.new("L", cropped.size)
        mask_draw = ImageDraw.Draw(mask)
        width, height = cropped.size
        mask_draw.ellipse((2.5, 2.5, width - 5, height - 5), fill=255)

        # add transparent background to mask
        cropped.putalpha(mask)
        return cropped

    def check_is_coloured(self, filename_without_extension):
        """Check if filename contains color suffix."""
        is_coloured = filename_without_extension.count("&") == 1

        if not is_coloured:
            self._append_ad_hoc_comment_to_log(
                f"{filename_without_extension} colour not specified. Processing in B&W format", self.log
            )

        return is_coloured

    def recolour_darken(self, cropped):
        """Apply darkening filter to image."""
        cropped = self._colour_sub(
            cropped, COLOURS["Black"]
        )  # black (darken the grey pixels so contrast is better when printed on paper)
        return cropped

    def determine_colour_extension(self, filename_without_extension):
        """Determine color extension from filename."""
        colour_extension = filename_without_extension[filename_without_extension.index("&") : -1]
        return colour_extension

    def recolour(self, cropped, filename_without_extension, colour_extension):
        """Apply color transformation to image."""
        # check for colour processing and sub if is_coloured is true

        match colour_extension:
            case "&R":
                cropped = self._colour_sub(cropped, COLOURS["R"])  # red
            case "&G":
                cropped = self._colour_sub(cropped, COLOURS["G"])  # medium sea green
            case "&B":
                cropped = self._colour_sub(cropped, COLOURS["B"])  # cornflour blue
            case "&P":
                cropped = self._colour_sub(cropped, COLOURS["P"])  # hot pink
            case "&PP":
                cropped = self._colour_sub(cropped, COLOURS["PP"])  # dark violet
            case "&E":  # make a copy for all colours
                self.recolour_create_each_colour(cropped, filename_without_extension)
                # exit out so we don't save the &E original picture in work handler
                return None

        # STANDARDISE THE SIZES OF STAMPS
        # post-recolour, we want to bring the images down to consistent dimensions
        cropped = self._standardise_size(cropped)
        return cropped

    def recolour_create_each_colour(self, cropped, filename_without_extension):
        """Create image variants in each available color."""
        # Need to iterate over all key:value pairs in std colours
        # we want to have one cropped image and recolour it for each standard colour
        # saving multiple copies

        for code, colour in COLOURS.items():
            colour_cropped = self._colour_sub(cropped.copy(), colour)
            colour_cropped = self._standardise_size(colour_cropped)
            colour_as_png = f"{filename_without_extension}{code}.png"
            self._save_image(colour_cropped, colour_as_png)


if __name__ == "__main__":
    pass
