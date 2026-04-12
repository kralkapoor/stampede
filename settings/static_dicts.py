"""Static configuration dictionaries for colors, paths, and settings."""

COLOURS = {
    "R": (255, 0, 0, 255),  # Red
    "G": (60, 179, 113, 255),  # Medium Sea Green
    "B": (100, 149, 237, 255),  # Cornflour Blue
    "P": (255, 105, 180, 255),  # Hot Pink
    "PP": (148, 0, 211, 255),  # Dark Violet
    "O": (250, 165, 25),  # Stampede Orange
    "Black": (0, 0, 0, 255),  # Just Black
}

RECT_PATHS = {
    "Custom": "1 Custom",
    "Black": "2 Black",
    "R": "3 Red",
    "P": "4 Hot Pink",
    "G": "5 Seagreen",
    "B": "6 Cornflour Blue",
    "PP": "7 Dark Violet",
    "O": "8 Orange",
}

VALID_FORMATS = ("jpg", "png", "jpeg", "webp")
IMAGE_QUALITY = 100
STANDARD_IMG_SIZE = None  # (200,200)
LOG_LOCATION = "settings/log.txt"

IMAGE_DIR = "img"
PROCESSED_DIR_CIRCLE = "img/Processed/Circles"
PROCESSED_DIR_RECT = "img/Processed/Rectangles"
PROCESSED_DIR_STICKER = "img/Processed/Stickers"
PROCESSED_DIR_AVATAR = "img/Processed/Avatars"
