"""View utility functions for GUI processing dialogs."""

import threading
import tkinter as tk
from tkinter import messagebox


def show_processing_dialog(master_window: tk.Tk, title: str, message: str, processing_callback):
    """
    Show a processing dialog with animation while executing a callback function.

    Args:
        master_window: The parent window
        title: Dialog title
        message: Message to display
        processing_callback: Function to execute in background

    Returns:
        Result from the processing_callback
    """
    # Create and show processing dialog
    processing_dialog = tk.Toplevel(master_window)
    processing_dialog.title(title)
    processing_dialog.geometry("300x100")
    processing_dialog.transient(master_window)
    processing_dialog.grab_set()

    # Center the dialog
    processing_dialog.update_idletasks()
    x = (processing_dialog.winfo_screenwidth() // 2) - (300 // 2)
    y = (processing_dialog.winfo_screenheight() // 2) - (100 // 2)
    processing_dialog.geometry(f"300x100+{x}+{y}")

    label = tk.Label(processing_dialog, text=message, font=("Arial", 12), fg="blue")
    label.pack(expand=True)

    # Progress indicator
    progress_var = tk.StringVar()
    progress_label = tk.Label(processing_dialog, textvariable=progress_var, font=("Arial", 10))
    progress_label.pack()

    # Storage for result and exception
    result_container = {"result": None, "exception": None}

    def animate_progress():
        while hasattr(animate_progress, "running") and animate_progress.running:
            for i in range(4):
                if hasattr(animate_progress, "running") and animate_progress.running:
                    progress_var.set("Processing" + "." * i)
                    processing_dialog.update()
                    processing_dialog.after(500)

    animate_progress.running = True

    def execute_request():
        try:
            result = processing_callback()
            result_container["result"] = result
            animate_progress.running = False
            processing_dialog.destroy()

            if result:
                messagebox.showinfo("Success", "Processing completed successfully!")
            else:
                messagebox.showerror("Error", "Processing failed. Check logs for details.")

        except Exception as e:
            result_container["exception"] = e
            animate_progress.running = False
            processing_dialog.destroy()
            messagebox.showerror("Error", f"Error during processing: {str(e)}")

    # Start animation
    threading.Thread(target=animate_progress, daemon=True).start()

    # Start processing in background
    threading.Thread(target=execute_request, daemon=True).start()

    # Keep dialog open until processing is done
    processing_dialog.wait_window()

    # Return result or raise exception
    if result_container["exception"] is not None:
        raise result_container["exception"]
    return result_container["result"]
