"""Avatar generation handler using OpenAI's image generation API."""

import base64
import os

from handling.avatar_base_handler import AvatarBaseHandler
from settings.avatar_prompt import BASE_PROMPT
from settings.static_dicts import IMAGE_DIR, PROCESSED_DIR_AVATAR


class AvatarHandler(AvatarBaseHandler):
    """Handles avatar image generation using OpenAI's API."""

    def __init__(self):
        """Initialize avatar handler."""
        super().__init__()
        self.prompt = BASE_PROMPT

    def process_avatar(self, user_prompt: str) -> list:
        """Process avatar generation. Returns list of processed image tuples."""
        self._append_ad_hoc_comment_to_log(f"Avatar handling with prompt: {user_prompt}")

        images_for_processing = self._get_input_images()
        try:
            result = self._execute_model_request(user_prompt, images_for_processing)
        finally:
            for file in images_for_processing:
                file.close()

        for file in images_for_processing:
            file_name = file.name.split("/")[-1]
            self._archive_image(file_name)
            print(f"Archived input image: {file_name}")

        return result

    def _get_input_images(self) -> list:
        input_files = [
            open(f"{IMAGE_DIR}/{file}", "rb") for file in os.listdir(IMAGE_DIR) if self._is_valid_file_type(file)
        ]
        return input_files

    def _execute_model_request(self, user_prompt: str, input_images: list) -> list:
        processed_images = []

        for image in input_images:
            res = super()._execute_edit_request(user_prompt, image)
            file_name = image.name.split("/")[-1]
            if res is None:
                self._append_ad_hoc_comment_to_log(f"Failed to generate avatar for: {file_name}\n")
                print(f"Failed to generate avatar for: {file_name}")
                continue
            processed_images.append((file_name, res))

        self._save_avatar(processed_images)
        return processed_images

    def _save_avatar(self, response_obj):
        for input_name, returned_image in response_obj:
            image_base64 = returned_image.b64_json
            image_bytes = base64.b64decode(image_base64)
            input_stem = os.path.splitext(input_name)[0]
            output_filename = f"{input_stem}_avatar.png"
            with open(f"{PROCESSED_DIR_AVATAR}/{output_filename}", "wb") as f:
                f.write(image_bytes)
            self._append_ad_hoc_comment_to_log(f"Saved avatar: {output_filename}")
