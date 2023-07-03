import tkinter as tk
from tkinter import PhotoImage
from PIL import ImageTk, Image
from ImageProcessor import Circles, Rectangles, Stickers

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Stampede")

        # Set the background color to black
        master.configure(bg='white')

        # Load logo and button images
        self.logo_image = ImageTk.PhotoImage(Image.open("logo.png"))
        self.rect_image = ImageTk.PhotoImage(Image.open("rectangle.png"))
        self.circle_image = ImageTk.PhotoImage(Image.open("circle.png"))
        self.sticker_image = ImageTk.PhotoImage(Image.open("sticker.png"))

        # Logo
        self.logo_label = tk.Label(master, image=self.logo_image, bg='black')
        self.logo_label.pack(side=tk.TOP)

        # Buttons
        self.rect_button = tk.Button(master, image=self.rect_image, command=self.process_rectangles, borderwidth=0)
        self.rect_button.pack(side=tk.LEFT)

        self.circle_button = tk.Button(master, image=self.circle_image, command=self.process_circles, borderwidth=0)
        self.circle_button.pack(side=tk.LEFT)

        self.sticker_button = tk.Button(master, image=self.sticker_image, command=self.process_stickers, borderwidth=0)
        self.sticker_button.pack(side=tk.LEFT)

    def process_rectangles(self):
        print('rectangles')
        # Instantiate Rectangles class and call pool_handler method
        # rects = Rectangles()
        # rects.pool_handler()

    def process_circles(self):
        print('circles')
        # Instantiate Circles class and call pool_handler method
        circles = Circles()
        circles.pool_handler()
        

    def process_stickers(self):
        print('stickers')
        # Instantiate Stamps class and call pool_handler method
        stamps = Stickers()
        stamps.pool_handler()

root = tk.Tk()
root.geometry("600x400")  # Set window size
root.resizable(False, False)  # Make window unresizable
gui = GUI(root)
root.mainloop()
