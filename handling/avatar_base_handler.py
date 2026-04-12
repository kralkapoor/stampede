"""Base avatar handler providing common OpenAI functionality."""

from handling.base_image_handler import BaseImageHandler
from handling.util.openai_util import create_openai_client
from openai.types.image import Image


class AvatarBaseHandler(BaseImageHandler):
    """Base class for avatar handlers with OpenAI integration."""

    def __init__(self):
        super().__init__()
        self.client = create_openai_client()

    def _execute_edit_request(self, user_prompt: str, image_data) -> Image:
        """Execute OpenAI image edit request with common parameters."""
        try:
            result = self.client.images.edit(
                model="gpt-image-1.5",
                image=image_data,
                prompt=user_prompt,
                background="transparent",
                n=1,
                quality="high",
                size="auto",
            )
            # Process a single avatar per request, i.e. each call is one in, one out
            return result.data[0]
        except Exception as e:
            print(f"Error in OpenAI API request: {e}")
            return None
