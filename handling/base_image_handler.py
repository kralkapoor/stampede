from multiprocessing import Pool
from datetime import datetime
import os
import tkinter as tk
from tkinter import messagebox
import threading
from settings.init_dirs import init_all
from settings.static_dicts import (
    valid_formats_cfg,
    image_quality_cfg,
    standard_img_size_cfg,
    log_location,
)


class BaseImageHandler:
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
        self.img_dir = os.listdir("./img")
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
        # Set to 4 to prevent DE lagging. Typically smaller quantities of pictures are loaded together.
        p = Pool(4)  # default processes = cpu_count().
        p.map(self.work_handler, imgs)

    def work_handler(self, file):
        """Defines the work to be done by the pool handler. Requires an override from a child class

        Args:
            file (Image): Each image in the img generator
        """
        print("Requires override")
        return

    def append_ad_hoc_comment_to_log(self, comment, log_file=log_location) -> None:
        with open(f"{log_file}", "a") as log:
            log.write(comment)
        return

    def append_processed_result_to_log(self, start_time: float, end_time: float, img_file, log_file: str):
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
        os.replace(f"img/{image_to_archive}", f"img/zArchive/{image_to_archive}")


if __name__ == "__main__":
    pass
