import tkinter as tk
from tkinter import PhotoImage
from PIL import ImageTk, Image
from ImageProcessor import Circles, Rectangles, Stickers

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Stampede Resizer")
        self.rects = Rectangles()
        self.circles = Circles()
        self.stamps = Stickers()

        # Set the background color to black
        master.configure(bg='white')

        # Load logo and button images
        self.logo_image = ImageTk.PhotoImage(Image.open("config/assets/logo.png"))

        # Logo
        self.logo_label = tk.Label(master, image=self.logo_image, bg='white')
        self.logo_label.pack(side=tk.TOP)

        # Bottom frame
        self.bottom_frame = tk.Frame(master,background='white')
        self.bottom_frame.pack(side=tk.BOTTOM, fill='none')

        # Buttons
        self.rect_button = tk.Button(self.bottom_frame, text='Rectangles', command=self.process_rectangles, borderwidth=0, background='lightblue', activebackground='yellow', width=7)
        self.rect_button.pack(side=tk.LEFT, expand=True, padx=5)

        self.circle_button = tk.Button(self.bottom_frame, text='Circles', command=self.process_circles, borderwidth=0, background='pink', activebackground='yellow', width=7)
        self.circle_button.pack(side=tk.LEFT, expand=True, padx=5)

        self.sticker_button = tk.Button(self.bottom_frame, text='Stickers', command=self.process_stickers, borderwidth=0, background='lightgreen', activebackground='yellow', width=7)
        self.sticker_button.pack(side=tk.LEFT, expand=True, padx=5)

    def process_rectangles(self):
        self.rects.pool_handler()
        exit(0)
        
    def process_circles(self):
        self.circles.pool_handler()
        exit(0)

    def process_stickers(self):
        # self.stamps.pool_handler()
        pass

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("313x200")  # Set window size
    root.resizable(False, False)  # Make window unresizable
    gui = GUI(root)
    root.mainloop()
