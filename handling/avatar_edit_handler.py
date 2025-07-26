"""Avatar editing handler using OpenAI's image editing API."""

import base64
import os
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

from PIL import Image, ImageTk

from handling.avatar_base_handler import AvatarBaseHandler
from handling.util.view_util import show_processing_dialog
from settings.avatar_prompt import BASE_PROMPT
from settings.static_dicts import PROCESSED_DIR_AVATAR


class AvatarEditHandler(AvatarBaseHandler):
    """Handles avatar image editing using OpenAI's image editing capabilities."""

    def __init__(self, master: tk.Tk):
        """Initialize avatar edit handler."""
        super().__init__()
        self.master_window = master
        self.prompt = BASE_PROMPT
        self.image_file = None

    def process_edit_avatar(self):
        """Process avatar editing requests."""
        # Validate exactly one image exists
        if not self._validate_single_image():
            return

        # Get user prompt with image preview
        user_prompt, window = self._get_prompt_with_preview()
        window.destroy()
        print(f"edit prompt = {user_prompt}")
        self._append_ad_hoc_comment_to_log(f"Avatar edit with prompt: {user_prompt}")

        with open(f"img/{self.image_file}", "rb") as image_data:

            # Show processing feedback and execute in background
            show_processing_dialog(
                self.master_window,
                "Processing...",
                "Processing image...\nPlease wait...",
                lambda: self._execute_edit_request(user_prompt, image_data),
            )

        # Archive the processed input image
        image_name = self.image_file.split("/")[-1]
        self._archive_image(image_name)
        print(f"Archived input image: {image_name}")

        # Exit
        self._exit_program()

    def _validate_single_image(self) -> bool:
        """Check that exactly one image file exists in img directory"""
        image_files = [file for file in os.listdir("img") if self._is_valid_file_type(file)]

        if len(image_files) == 0:
            messagebox.showerror(
                "No Image Found", "Please place exactly one image file in the img directory for editing."
            )
            return False
        if len(image_files) > 1:
            messagebox.showerror(
                "Multiple Images Found",
                f"{len(image_files)} images in img directory. Please ensure only one image is present for editing.",
            )
            return False

        self.image_file = image_files[0]
        return True

    def _get_prompt_with_preview(self) -> tuple[str, tk.Toplevel]:
        prompt_set = tk.BooleanVar(value=False)

        # Create a child window that spawns from the master frame
        child_window = tk.Toplevel(self.master_window)
        child_window.geometry("1200x600")
        child_window.title("Edit Avatar - Modify Existing Image")

        # Create main frame to hold image and text side by side
        main_frame = tk.Frame(child_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left frame for image preview
        image_frame = tk.Frame(main_frame)
        image_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))

        # Right frame for text prompt
        text_frame = tk.Frame(main_frame)
        text_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Load and display image
        try:
            image_path = f"img/{self.image_file}"
            pil_image = Image.open(image_path)

            # Resize image for preview (max 300x300)
            pil_image.thumbnail((300, 300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(pil_image)

            image_label = tk.Label(image_frame, image=photo)
            image_label.image = photo  # Keep a reference
            image_label.pack()

            # Add filename label
            filename_label = tk.Label(image_frame, text=f"Editing: {self.image_file}", font=("Arial", 10, "bold"))
            filename_label.pack(pady=(5, 0))

        except Exception as e:
            error_label = tk.Label(image_frame, text=f"Error loading image:\n{str(e)}", fg="red")
            error_label.pack()

        # Text area for prompt
        prompt_label = tk.Label(
            text_frame, text="Describe how you want to modify this image:", font=("Arial", 12, "bold")
        )
        prompt_label.pack(anchor="w", pady=(0, 5))

        text: tk.Text = tk.Text(text_frame, wrap="word", height=20, width=60)
        text.insert(tk.INSERT, "Please modify this image by: ")
        text.pack(fill=tk.BOTH, expand=True)

        # Bottom frame for buttons
        bottom_frame = tk.Frame(child_window)
        bottom_frame.pack(side=tk.BOTTOM, pady=10)

        # Buttons
        ok: tk.Button = tk.Button(
            master=bottom_frame,
            text="Edit Image",
            command=lambda: prompt_set.set(True),
            width=12,
            background="green",
            font=("Arial", 10, "bold"),
        )
        ok.pack(side=tk.RIGHT, expand=True, padx=5)

        cancel: tk.Button = tk.Button(
            master=bottom_frame,
            text="Cancel",
            command=self._exit_program,
            width=12,
            background="red",
            font=("Arial", 10, "bold"),
        )
        cancel.pack(side=tk.LEFT, expand=True, padx=5)

        # Wait on an ok before setting the prompt
        ok.wait_variable(prompt_set)

        return text.get("1.0", tk.END), child_window

    def _execute_edit_request(self, user_prompt: str, image_data) -> list:
        try:
            result_data = super()._execute_edit_request(user_prompt, image_data)
            if not result_data:
                return []

            # Save the edited image - expect b64_json response like avatar_handler
            for returned_image in result_data:
                image_base64 = returned_image.b64_json
                image_bytes = base64.b64decode(image_base64)
                # Save the image to a file with timestamp prefix
                timestamp = datetime.now().strftime("%Y%m%d_%H%M")
                output_filename = f"{timestamp}_edited.png"
                with open(f"{PROCESSED_DIR_AVATAR}/{output_filename}", "wb") as f:
                    f.write(image_bytes)
                print(f"Saved edited image: {output_filename}")

            return result_data

        except Exception as e:
            self._append_ad_hoc_comment_to_log(f"Error in edit request: {str(e)}")
            print(f"Error in edit request: {str(e)}")
            return []

    def _exit_program(self):
        exit(0)
