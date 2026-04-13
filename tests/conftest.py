"""Shared test fixtures for handler unit tests.

All handler constructors hit the filesystem (init_directories, os.listdir).
The autouse fixture below patches these globally so any handler can be
instantiated in tests without a real img/ directory.
"""

import base64
import io
from unittest.mock import MagicMock, patch

import pytest
from PIL import Image


@pytest.fixture(autouse=True)
def patch_handler_init():
    """Automatically patches filesystem calls made during handler __init__.

    Without this, every handler constructor would fail because it tries to
    create directories and list files in img/.
    """
    with (
        patch("settings.init_dirs.init_directories"),
        patch("handling.base_image_handler.os.listdir", return_value=[]),
    ):
        yield


@pytest.fixture
def mock_openai_client():
    """Patches the OpenAI client factory so avatar handlers can be instantiated."""
    with patch("handling.avatar_base_handler.create_openai_client", return_value=MagicMock()):
        yield


@pytest.fixture
def base_handler():
    from handling.base_image_handler import BaseImageHandler

    return BaseImageHandler()


@pytest.fixture
def circle_handler():
    from handling.imagehandler.circle_handler import CircleHandler

    return CircleHandler()


@pytest.fixture
def rectangle_handler():
    from handling.imagehandler.rectangle_handler import RectangleHandler

    return RectangleHandler()


@pytest.fixture
def avatar_handler(mock_openai_client):
    from handling.avatar_handler import AvatarHandler

    return AvatarHandler()


@pytest.fixture
def avatar_edit_handler(mock_openai_client):
    from handling.avatar_edit_handler import AvatarEditHandler

    return AvatarEditHandler()


@pytest.fixture
def small_rgba_image():
    """A real 10x10 RGBA PIL Image for pixel-level testing."""
    return Image.new("RGBA", (10, 10), (100, 100, 100, 255))


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI image response with a valid base64 PNG.

    Mirrors the structure returned by client.images.edit().data[0],
    which has a .b64_json attribute containing the encoded image.
    """
    img = Image.new("RGBA", (1, 1), (0, 0, 0, 255))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()

    response = MagicMock()
    response.b64_json = b64
    return response
