import os
import time

from PIL import Image, ImageDraw

from handling.base_image_handler import BaseImageHandler
from settings.static_dicts import COLOURS, PROCESSED_DIR_RECT, RECT_PATHS


class RectangleHandler(BaseImageHandler):

    def __init__(self):
        super().__init__()
        self.rect_paths = RECT_PATHS

    def pool_handler(self):
        super().pool_handler()
        self.open_save_destination()
        return

    def open_save_destination(self) -> None:
        if os.name == "nt":
            abs_path = os.path.realpath(PROCESSED_DIR_RECT)
            try:
                os.startfile(abs_path)
            except Exception as e:
                print("something wrong with opening explorer on open save destination")
        return

    # Override super.work_handler for rectangles specifically
    def _work_handler(self, file):
        # Convert valid formats to png to allow RGBA
        start = time.time()
        no_extension = file[: file.index(".") + 1]
        as_png = f"{no_extension}png"

        try:
            os.rename(f"img/{file}", f"img/{as_png}")
        except FileExistsError:
            with open(self.log, "a") as log:
                log.write(f'{self.now.strftime("%d/%m/%Y, %H:%M:%S")}: "{as_png}" ERROR! FILE ALREADY EXISTS\n')
            return
        try:
            image = Image.open(f"img/{as_png}")
            canvas = Image.new("RGBA", image.size, (255, 255, 255, 255))
            ImageDraw.Draw(canvas)
            canvas.paste(image)

            # check for custom stamp to determine one or many colours
            custom_stamp = False
            try:
                custom_stamp = no_extension.count("&") == 1
            except ValueError:
                print(f"Processing {as_png} as generic stamp - all colours")

            path = ""
            if custom_stamp:
                path = self.rect_paths["Custom"]
                match no_extension[no_extension.index("&") : -1]:
                    case "&R":
                        canvas = self._colour_sub(canvas, COLOURS["R"])  # red
                    case "&G":
                        canvas = self._colour_sub(canvas, COLOURS["G"])  # medium sea green
                    case "&B":
                        canvas = self._colour_sub(canvas, COLOURS["B"])  # cornflour blue
                    case "&P":
                        canvas = self._colour_sub(canvas, COLOURS["P"])  # hot pink
                    case "&PP":
                        canvas = self._colour_sub(canvas, COLOURS["PP"])  # dark violet
                    case _:
                        canvas = self._colour_sub(canvas, COLOURS["Black"])  # default to black if not specified

                canvas.save(f"img/Processed/Rectangles/{path}/{as_png}", quality=100)

                # Write to log
                self._append_processed_result_to_log(start, time.time(), as_png, self.log)

            # If it's not a custom stamp, then create a copy in each standard colour
            else:
                for code, colour_value in COLOURS.items():
                    rect_img = self._colour_sub(canvas.copy(), colour_value)
                    rect_img.save(
                        f"img/Processed/Rectangles/{self.rect_paths[code]}/{no_extension[:-1]}&{code}.png",
                        quality=self.quality_val,
                    )

                self._append_processed_result_to_log(start, time.time(), as_png, self.log)

            self.open_save_destination()

            # Archive
            self._archive_image(as_png)

        except Exception as e:
            with open(self.log, "a") as log:
                log.write(f'{self.now.strftime("%d/%m/%Y %H:%M")}: UNEXPECTED ERROR PROCESSING {as_png}\n')
                log.write(f"    Reason: {e}\n")


if __name__ == "__main__":
    pass
