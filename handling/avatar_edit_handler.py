"""Avatar editing handler using OpenAI's image editing API."""

import base64
import logging
import os
from datetime import datetime

from handling.avatar_base_handler import AvatarBaseHandler
from settings.static_dicts import PROCESSED_DIR_AVATAR

logger = logging.getLogger(__name__)


class AvatarEditHandler(AvatarBaseHandler):
    """Handles avatar image editing using OpenAI's image editing capabilities."""

    def __init__(self):
        """Initialize avatar edit handler."""
        super().__init__()

    def validate_single_image(self) -> str:
        """Check that exactly one image file exists in img directory.

        Returns:
            The image filename.

        Raises:
            ValueError: If zero or more than one image is found.
        """
        image_files = [file for file in os.listdir("img") if self._is_valid_file_type(file)]

        if len(image_files) == 0:
            raise ValueError("No image found. Place exactly one image file in the img directory for editing.")
        if len(image_files) > 1:
            raise ValueError(
                f"{len(image_files)} images in img directory. Please ensure only one image is present for editing."
            )

        return image_files[0]

    def process_edit_avatar(self, user_prompt: str, image_file: str):
        """Process avatar editing.

        Args:
            user_prompt: The editing instruction from the user.
            image_file: Filename of the image in img/ to edit.

        Returns:
            The result data from the API, or empty list on failure.
        """
        logger.info("Editing avatar with prompt: %s", user_prompt)

        with open(f"img/{image_file}", "rb") as image_data:
            result = self._execute_edit_request(user_prompt, image_data)

        if not result:
            return None

        self._save_edited_avatar(result)
        self._archive_image(image_file)
        logger.info("Archived input image: %s", image_file)

        return result

    def _save_edited_avatar(self, returned_image):
        image_base64 = returned_image.b64_json
        image_bytes = base64.b64decode(image_base64)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        output_filename = f"{timestamp}_edited.png"
        with open(f"{PROCESSED_DIR_AVATAR}/{output_filename}", "wb") as f:
            f.write(image_bytes)
        logger.info("Saved edited image: %s", output_filename)
