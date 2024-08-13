import tkinter as tk

panel = None

def update_image_display(img):
    global panel
    if panel is not None and panel.winfo_exists():
        panel.configure(image=img)
        panel.image = img
    else:
        panel = tk.Label(panel, image=img)
        panel.image = img
        panel.pack()
