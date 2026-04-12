"""Base image handler providing common functionality for image processing."""

import os
from datetime import datetime
from multiprocessing import Pool

from settings.init_dirs import init_directories
from settings.static_dicts import (
    IMAGE_QUALITY,
    LOG_LOCATION,
    STANDARD_IMG_SIZE,
    VALID_FORMATS,
)


class BaseImageHandler:
    """Base class for all image handlers with multiprocessing and logging."""

    def __init__(self):
        init_directories()  # init prerequisite directories that are gitignored
        self.valid_formats = VALID_FORMATS
        self.quality_val = IMAGE_QUALITY
        self.standard_size = STANDARD_IMG_SIZE
        # Current values
        self.curr_width = 0
        self.curr_height = 0
        self.curr_canvas_size = (0, 0)
        self.now = datetime.now()
        self.img_dir = os.listdir("./img")
        self.log = LOG_LOCATION
        # self.max_cores = multiprocessing.cpu_count()

    def execute(self):
        """
        Pool wrapper that performs the work for processing. Applies the _handler_function method to each files
        """
        imgs = self._get_input_images()
        # Set to 4 to prevent DE lagging. Typically smaller quantities of pictures are loaded together.
        p = Pool(4)  # default processes = cpu_count().
        p.map(self._handler_function, imgs)

    def _handler_function(self, file):
        """Defines the work to be done by the execute method. Requires an override from a child class

        Args:
            file (Image): Each image in the img generator
        """
        print("Requires override")

    def _get_input_images(self) -> list[str]:
        """
        Loops through the img directory to identify suitable images

        Returns:
            List: of all the images for processing
        """
        files = [file for file in self.img_dir if self._is_valid_file_type(file)]
        return files

    def _append_ad_hoc_comment_to_log(self, comment, log_file=LOG_LOCATION) -> None:
        with open(f"{log_file}", "a", encoding="utf-8") as log:
            log.write(comment)

    def _append_processed_result_to_log(self, start_time: float, end_time: float, img_file, log_file: str):
        """Append a message to the log saying whether the img was successfully processed or not

        Args:
            start_time (float): the time that the execute method was executed
            end_time (float): the time the execute method completed
            img_file (_type_): each image file in the img generator
            log_file (str): the name of the log in ./config
        """
        with open(f"{log_file}", "a", encoding="utf-8") as log:
            log.write(
                f'{self.now.strftime("%d/%m/%Y %H:%M")}: {img_file} processed in {round(end_time - start_time, 2)}s\n'
            )

    def _colour_sub(self, image, colour: tuple):
        """Method to replace pixels over a certain opacity with that of another specified colour

        Args:
            image (Image): The image to have its pixels replaced
            colour (tuple): New colour as a tuple (R,G,B,Opacity)

        Returns:
            Image: Recoloured image
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
                print("something wrong with opening explorer on open save destination")

    def _rename_file(self, file: str, new_name: str) -> bool:
        """Rename file from old to new name."""
        try:
            os.rename(f"img/{file}", f"img/{new_name}")
            return True
        except FileExistsError:
            self._append_ad_hoc_comment_to_log(
                f'{self.now.strftime("%d/%m/%Y, %H:%M:%S")}: "{new_name}" ERROR! FILE ALREADY EXISTS\n'
            )
            return False

    def _archive_image(self, image_to_archive):
        """Moves the image to the archive folder (currently hardcoded)

        Args:
            image_to_archive (Image): Image to archive
        """
        try:
            os.replace(f"img/{image_to_archive}", f"img/zArchive/{image_to_archive}")
        except OSError as e:
            self._append_ad_hoc_comment_to_log(f"Unable to archive {image_to_archive}: {str(e)}")

    def _is_valid_file_type(self, file_name: str):
        if not file_name:
            return False
        return file_name.lower().endswith(VALID_FORMATS)


if __name__ == "__main__":
    pass
