import tkinter as tk
from tkinter import Tk

from PIL import Image, ImageTk

from handling.avatar_edit_handler import AvatarEditHandler
from handling.avatar_handler import AvatarHandler
from handling.imagehandler.circle_handler import CircleHandler
from handling.imagehandler.circle_sticker_handler import CircleStickerHandler
from handling.imagehandler.rectangle_handler import RectangleHandler


class GUI:
    def __init__(self, master: Tk):
        self.master = master
        master.title("Stampede Resizer")
        self.rects = RectangleHandler()
        self.circles = CircleHandler()
        self.stickers = CircleStickerHandler()
        self.avatar = AvatarHandler(master)
        self.avatar_edit = AvatarEditHandler(master)

        # Set the background color to black
        master.configure(bg="white")

        # Load logo and button images
        self.logo_image = ImageTk.PhotoImage(Image.open("assets/logo.png"))

        # Logo
        self.logo_label = tk.Label(master, image=self.logo_image, bg="white")
        self.logo_label.pack(side=tk.TOP)

        # Bottom frame
        self.bottom_frame = tk.Frame(master, background="white")
        self.bottom_frame.pack(side=tk.BOTTOM, fill="none")

        # Buttons
        self.rect_button = tk.Button(
            self.bottom_frame,
            text="Rectangles",
            command=self.process_rectangles,
            borderwidth=0,
            background="lightblue",
            activebackground="yellow",
            width=7,
        )
        self.rect_button.pack(side=tk.LEFT, expand=True, padx=5)

        self.circle_button = tk.Button(
            self.bottom_frame,
            text="Circles",
            command=self.process_circles,
            borderwidth=0,
            background="pink",
            activebackground="yellow",
            width=7,
        )
        self.circle_button.pack(side=tk.LEFT, expand=True, padx=5)

        self.sticker_button = tk.Button(
            self.bottom_frame,
            text="Stickers",
            command=self.process_stickers,
            borderwidth=0,
            background="lightgreen",
            activebackground="yellow",
            width=7,
        )
        self.sticker_button.pack(side=tk.LEFT, expand=True, padx=5)

        self.new_avatar_button = tk.Button(
            self.bottom_frame,
            text="New Avatar",
            command=self.process_avatar,
            borderwidth=0,
            background="firebrick1",
            activebackground="yellow",
            width=9,
        )
        self.new_avatar_button.pack(side=tk.LEFT, expand=True, padx=5)

        self.edit_avatar_button = tk.Button(
            self.bottom_frame,
            text="Edit Avatar",
            command=self.process_edit_avatar,
            borderwidth=0,
            background="orange",
            activebackground="yellow",
            width=9,
        )
        self.edit_avatar_button.pack(side=tk.LEFT, expand=True, padx=5)

    def process_rectangles(self):
        self.rects.pool_handler()
        exit(0)

    def process_circles(self):
        self.circles.pool_handler()
        exit(0)

    def process_stickers(self):
        self.stickers.pool_handler()
        exit(0)

    def process_avatar(self):
        self.avatar.process_avatar()

    def process_edit_avatar(self):
        self.avatar_edit.process_edit_avatar()


if __name__ == "__main__":
    root: Tk = tk.Tk()
    root.geometry("550x200")  # Set window size - expanded for new buttons
    root.resizable(True, True)
    gui: GUI = GUI(root)
    root.mainloop()
