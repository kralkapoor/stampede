"""Avatar generation handler using OpenAI's image generation API."""

import base64
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from handling.avatar_base_handler import AvatarBaseHandler
from settings.avatar_prompt import BASE_PROMPT
from settings.static_dicts import IMAGE_DIR, PROCESSED_DIR_AVATAR

logger = logging.getLogger(__name__)


class AvatarHandler(AvatarBaseHandler):
    """Handles avatar image generation using OpenAI's API."""

    def __init__(self):
        """Initialize avatar handler."""
        super().__init__()
        self.prompt = BASE_PROMPT
        self.input_files = []

    def process_avatar(self, user_prompt: str) -> None:
        """Process avatar generation.

        :param user_prompt: The generation prompt from the user.
        :type user_prompt: str
        """
        logger.info("Generating avatars with prompt: %s", user_prompt)

        input_images = self._get_input_files()
        try:
            processed_images = self._execute_model_requests(user_prompt, input_images)
            # Close opened files to prevent conflicts during archiving
            self._close_input_files()

            self._save_avatars(processed_images)
            for file_name, _ in processed_images:
                self._archive_image(file_name)
                logger.info("Archived input image: %s", file_name)

        except Exception as e:
            logger.error("Failure during avatar processing: %s", e)

    def _get_input_files(self) -> list:
        self.input_files = [
            open(f"{IMAGE_DIR}/{file}", "rb") for file in os.listdir(IMAGE_DIR) if self._is_valid_file_type(file)
        ]
        return self.input_files

    def _close_input_files(self) -> None:
        for file in self.input_files:
            file.close()

    def _execute_model_requests(self, user_prompt: str, input_images: list) -> list:
        processed_images = []
        # Bind to local var because super() doesn't resolve correctly inside threads
        edit_request = self._execute_edit_request

        # Make concurrent api calls to prevent waiting on sequential completion
        with ThreadPoolExecutor() as executor:
            futures = {}
            for image in input_images:
                future = executor.submit(edit_request, user_prompt, image)
                file_name = image.name.split("/")[-1]
                futures[future] = file_name

            for future in as_completed(futures):
                file_name = futures[future]
                result = future.result()

                if result is None:
                    logger.error("Failed to generate avatar for: %s", file_name)
                    continue

                processed_images.append((file_name, result))

        return processed_images

    def _save_avatars(self, processed_data: list[tuple]):
        for input_name, returned_image in processed_data:
            image_base64 = returned_image.b64_json
            image_bytes = base64.b64decode(image_base64)
            input_stem = os.path.splitext(input_name)[0]
            output_filename = f"{input_stem}_avatar.png"
            with open(f"{PROCESSED_DIR_AVATAR}/{output_filename}", "wb") as f:
                f.write(image_bytes)
            logger.info("Saved avatar: %s", output_filename)
