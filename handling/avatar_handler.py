"""Avatar generation handler using OpenAI's image generation API."""

import base64
import os
import tkinter as tk
from datetime import datetime

from handling.avatar_base_handler import AvatarBaseHandler
from handling.util.view_util import show_processing_dialog
from settings.avatar_prompt import BASE_PROMPT
from settings.static_dicts import EXAMPLE_DIR_AVATAR, IMAGE_DIR, PROCESSED_DIR_AVATAR


class AvatarHandler(AvatarBaseHandler):
    """Handles avatar image generation using OpenAI's API."""

    def __init__(self, master: tk.Tk):
        """Initialize avatar handler."""
        super().__init__()
        self.master_window = master
        self.prompt = BASE_PROMPT

    def process_avatar(self):
        """Process avatar generation requests."""
        # Get user prompt with modifications, if any
        user_prompt, window = self._get_prompt()
        window.destroy()
        print(f"prompt = {user_prompt}")
        self._append_ad_hoc_comment_to_log(f"Avatar handling with prompt: {user_prompt}")

        images_for_processing = self._fetch_imgs_as_binary()

        show_processing_dialog(
            self.master_window,
            "Processing...",
            "Generating avatar...\nPlease wait...",
            lambda: self._execute_model_request(user_prompt, images_for_processing),
        )

        # Archive all processed input images (files are now closed)
        # Files are bytes here
        for file in images_for_processing:
            # Don't want to archive the exeplar images
            if EXAMPLE_DIR_AVATAR in file.name:
                continue
            file_name = file.name.split("/")[-1]  # Only need the actual filename, not entire path
            self._archive_image(file_name)
            print(f"Archived input image: {file_name}")
        # Exit
        self._exit_program()

    def _get_prompt(self) -> tuple[str, tk.Toplevel]:
        prompt_set = tk.BooleanVar(value=False)

        # Create a child window that spawns from the master frame
        child_window = tk.Toplevel(self.master_window)
        child_window.geometry("1000x400")
        child_window.title("Avatar Processing Instructions")

        # Bottom frame to place buttons
        bottom_frame = tk.Frame(child_window)
        bottom_frame.pack(side=tk.BOTTOM)

        # Pack a text widget for hosting the prompt
        text: tk.Text = tk.Text(child_window, wrap="word", width=1000, height=20)
        text.insert(tk.INSERT, self.prompt)
        text.pack()

        # Set prompt_set to True to continue
        ok: tk.Button = tk.Button(
            master=bottom_frame, text="OK", command=lambda: prompt_set.set(True), width=7, background="green"
        )
        ok.pack(side=tk.RIGHT, expand=True, padx=5)
        cancel: tk.Button = tk.Button(
            master=bottom_frame, text="Cancel", command=self._exit_program, width=7, background="red"
        )
        cancel.pack(side=tk.LEFT, expand=True, padx=5)

        # Wait on an ok before setting the prompt
        ok.wait_variable(prompt_set)

        return text.get("1.0", tk.END), child_window

    def _fetch_imgs_as_binary(self) -> list:
        # Get list of input files first
        input_files = [
            open(f"{IMAGE_DIR}/{file}", "rb") for file in os.listdir(IMAGE_DIR) if self._is_valid_file_type(file)
        ]
        # Open exemplar images
        exemplar_images = [
            open(f"{EXAMPLE_DIR_AVATAR}/{file}", "rb")
            for file in os.listdir(EXAMPLE_DIR_AVATAR)
            if self._is_valid_file_type(file)
        ]

        return exemplar_images + input_files

    def _execute_model_request(self, user_prompt: str, images: list) -> list:
        try:
            result_data = super()._execute_edit_request(user_prompt, images)
            if not result_data:
                return []

            self._save_avatar_data(result_data)
            return result_data

        except Exception as e:
            self._append_ad_hoc_comment_to_log(f"Error in avatar generation: {str(e)}")
            print(f"Error in avatar generation: {str(e)}")
            return []

    def _save_avatar_data(self, result_data):
        for returned_image in result_data:
            image_base64 = returned_image.b64_json
            image_bytes = base64.b64decode(image_base64)
            # Save the image to a file with timestamp prefix
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            output_filename = f"{timestamp}.png"
            with open(f"{PROCESSED_DIR_AVATAR}/{output_filename}", "wb") as f:
                f.write(image_bytes)
            self._append_ad_hoc_comment_to_log(f"Saved avatar: {output_filename}")

    def _exit_program(self):
        exit(0)
