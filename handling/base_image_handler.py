import os
from datetime import datetime
from multiprocessing import Pool

from settings.init_dirs import init_all
from settings.static_dicts import IMAGE_QUALITY, LOG_LOCATION, STANDARD_IMG_SIZE, VALID_FORMATS


class BaseImageHandler:
    def __init__(self):
        init_all()  # init prerequisite directories that are gitignored
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

    def pool_handler(self):
        """
        Performs the work for processing. Applies the work_handler method to each file in the images generator
        """
        imgs = self._fetch_imgs_as_binary()
        # Set to 4 to prevent DE lagging. Typically smaller quantities of pictures are loaded together.
        p = Pool(4)  # default processes = cpu_count().
        p.map(self._work_handler, imgs)

    def _fetch_imgs_as_binary(self):
        """
        Loops through the img directory to identify suitable images

        Returns:
            Generator: of all the images for processing
        """
        files = (file for file in self.img_dir if self._is_valid_file_type(file))
        return files

    def _work_handler(self, file):
        """Defines the work to be done by the pool handler. Requires an override from a child class

        Args:
            file (Image): Each image in the img generator
        """
        print("Requires override")
        return

    def _append_ad_hoc_comment_to_log(self, comment, log_file=LOG_LOCATION) -> None:
        with open(f"{log_file}", "a") as log:
            log.write(comment)
        return

    def _append_processed_result_to_log(self, start_time: float, end_time: float, img_file, log_file: str):
        """Append a message to the log saying whether the img was successfully processed or not

        Args:
            start_time (float): the time that the pool handler was executed
            end_time (float): the time the pool handler completed
            img_file (_type_): each image file in the img generator
            log_file (str): the name of the log in ./config
        """
        with open(f"{log_file}", "a") as log:
            log.write(
                f'{self.now.strftime("%d/%m/%Y %H:%M")}: {img_file} processed in {round(end_time - start_time, 2)}s\n'
            )

    def _colour_sub(self, image, colour: tuple):
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
