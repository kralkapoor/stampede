import base64
from openai import OpenAI
from dotenv import load_dotenv
import os
from handling.exception.configuration_error import ConfigurationError
from settings.avatar_prompt import BASE_PROMPT
from uuid import uuid4
import tkinter as tk
from tkinter import messagebox
from .base_image_handler import BaseImageHandler
from settings.static_dicts import avatar_dir_on_process, avatar_exemplars_dir


class AvatarHandler(BaseImageHandler):

    def __init__(self, master: tk.Tk):
        self.master_window = master
        self.prompt = BASE_PROMPT
        self.client = self._create_client()

    def process_avatar(self):
        # Get user prompt with modifications, if any
        user_prompt, window = self._get_prompt()
        window.destroy()
        print(f'prompt = {user_prompt}')
        self.append_ad_hoc_comment_to_log(f"Avatar handling with prompt: {user_prompt}")

        ok = messagebox.askokcancel("Execute", "Generate Avatar?")
        if ok:
            self._execute_model_request(user_prompt)
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
        ok : tk.Button = tk.Button(master=bottom_frame, text="OK", command=lambda: prompt_set.set(True), width=7, background='green')
        ok.pack(side=tk.RIGHT, expand=True, padx=5)
        cancel: tk.Button = tk.Button(master=bottom_frame, text="Cancel", command=self._exit_program, width=7, background='red')
        cancel.pack(side=tk.LEFT, expand=True, padx=5)

        # Wait on an ok before setting the prompt
        ok.wait_variable(prompt_set)

        return text.get("1.0", tk.END), child_window
    
    def _execute_model_request(self, user_prompt: str) -> None:
        exemplar_images = [
            open(f'{avatar_exemplars_dir}/{file}', "rb") for file in os.listdir(avatar_exemplars_dir)
        ]
        input_images = [open(f'img/{file}', "rb") for file in os.listdir("img") if file.endswith("png") or file.endswith("jpg") or file.endswith("jpeg")]
        for img in input_images:
            exemplar_images.append(img)

        result = self.client.images.edit(
            model="gpt-image-1",
            image=exemplar_images,
            prompt=user_prompt,
            background="transparent",
            n=len(input_images),
            quality="medium",
            size="auto"
        )

        for returned_image in result.data:
            image_base64 = returned_image.b64_json
            image_bytes = base64.b64decode(image_base64)
            # Save the image to a file
            with open(f'{avatar_dir_on_process}/{str(uuid4())}.png', "wb") as f:
                f.write(image_bytes)

        return True

    def _create_client(self):
        load_dotenv()
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if OPENAI_API_KEY is None:
            raise ConfigurationError("No API key was loaded to the system environment")
        client = OpenAI(api_key=OPENAI_API_KEY)
        return client
    
    def _exit_program(self):
        exit(0)






