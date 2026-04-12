"""Base image handler providing common functionality for image processing."""

import logging
import os

from PIL import Image

from settings.init_dirs import init_directories
from settings.static_dicts import (IMAGE_QUALITY, STANDARD_IMG_SIZE,
                                   VALID_FORMATS)

logger = logging.getLogger(__name__)


class BaseImageHandler:
    """Base class for all image handlers."""

    def __init__(self):
        init_directories()  # init prerequisite directories that are gitignored
        self.valid_formats = VALID_FORMATS
        self.quality_val = IMAGE_QUALITY
        self.standard_size = STANDARD_IMG_SIZE
        # Current values
        self.curr_width = 0
        self.curr_height = 0
        self.curr_canvas_size = (0, 0)
        self.img_dir = os.listdir("./img")

    def execute(self):
        """Process all valid input images sequentially."""
        imgs = self._get_input_images()
        for img in imgs:
            self._handler_function(img)

    def _handler_function(self, file):
        """Defines the work to be done by the execute method. Requires an override from a child class.

        :param file: Each image in the img generator.
        :type file: Image
        """
        raise NotImplementedError

    def _get_input_images(self) -> list[str]:
        """Loops through the img directory to identify suitable images.

        :returns: All the images for processing.
        :rtype: list[str]
        """
        files = [file for file in self.img_dir if self._is_valid_file_type(file)]
        return files

    def _colour_sub(self, image: Image, colour: tuple) -> Image:
        """Replace pixels over a certain opacity with that of another specified colour.

        :param image: The image to have its pixels replaced.
        :type image: Image
        :param colour: New colour as a tuple (R,G,B,Opacity).
        :type colour: tuple
        :returns: Recoloured image.
        :rtype: Image
        """
        pixel_data = image.get_flattened_data()
        new_image = []

        for data in pixel_data:
            if data[3] != 0 and data[0] < 200:
                new_image.append(colour)
            else:
                new_image.append(data)

        image.putdata(new_image)
        return image

    def _open_save_destination(self, processed_dir: str) -> None:
        """Open save destination folder in file explorer."""
        if os.name == "nt":
            abs_path = os.path.realpath(processed_dir)
            try:
                os.startfile(abs_path)  # pylint: disable=no-member
            except Exception:
                logger.error("Failed to open save destination: %s", processed_dir)

    def _rename_file(self, file: str, new_name: str) -> bool:
        """Rename file from old to new name."""
        try:
            os.rename(f"img/{file}", f"img/{new_name}")
            return True
        except FileExistsError:
            logger.error("Rename failed, file already exists: %s", new_name)
            return False

    def _archive_image(self, image_to_archive):
        """Moves the image to the archive folder (currently hardcoded).

        :param image_to_archive: Image to archive.
        :type image_to_archive: Image
        """
        try:
            os.replace(f"img/{image_to_archive}", f"img/zArchive/{image_to_archive}")
        except OSError as e:
            logger.error("Failed to archive %s: %s", image_to_archive, e)

    def _is_valid_file_type(self, file_name: str):
        if not file_name:
            return False
        return file_name.lower().endswith(VALID_FORMATS)


if __name__ == "__main__":
    pass
