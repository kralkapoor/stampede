"""Base avatar handler providing common OpenAI functionality."""

import logging
import mimetypes

from openai.types.image import Image

from handling.base_image_handler import BaseImageHandler
from handling.util.openai_util import create_openai_client

logger = logging.getLogger(__name__)

# Ensure all image formats accepted by the OpenAI image model are registered
# Python on Windows doesn't always include webp, and other platforms may have gaps
mimetypes.add_type("image/png", ".png")
mimetypes.add_type("image/jpeg", ".jpg")
mimetypes.add_type("image/jpeg", ".jpeg")
mimetypes.add_type("image/webp", ".webp")


class AvatarBaseHandler(BaseImageHandler):
    """Base class for avatar handlers with OpenAI integration."""

    def __init__(self):
        super().__init__()
        self.client = create_openai_client()

    def _execute_edit_request(self, user_prompt: str, image_data) -> Image:
        """Execute OpenAI image edit request with common parameters."""
        try:
            result = self.client.images.edit(
                model="gpt-image-2",
                image=image_data,
                prompt=user_prompt,
                # Transparent bg not currently supported by gpt-image-2?
                # background="transparent",
                n=1,
                quality="high",
                size="1024x1024",
            )
            # Process a single avatar per request, i.e. each call is one in, one out
            return result.data[0]
        except Exception:
            logger.exception("OpenAI API request failed")
            return None
