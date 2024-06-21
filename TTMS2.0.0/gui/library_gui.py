import cv2
import tkinter as tk
from tkinter import Toplevel, simpledialog, filedialog, messagebox, Label, Button, Frame, Canvas, Scrollbar
from PIL import Image, ImageTk
from utils.file_utils import save_inventory_to_db, load_inventory_from_db, check_case_table_exists

library_window_open = False

def open_library_window(root):
    global library_window_open
    library_window = Toplevel(root)
    library_window.title("Image Library")
    library_window.geometry("600x600")
    
    def close_library_window():
        global library_window_open
        library_window_open = False
        library_window.destroy()

    library_window.protocol("WM_DELETE_WINDOW", close_library_window)

    def upload_image():
        if not check_case_table_exists():
            messagebox.showerror("Error", "No case table exists. Please create or load a case first.")
            return

        file_path = filedialog.askopenfilename()
        if file_path:
            label = simpledialog.askstring("Label Image", "Enter the label for this image:", parent=library_window)
            brand = simpledialog.askstring("Brand", "Enter the brand name", parent=library_window)
            size = simpledialog.askstring("Size", "Enter the shoe size", parent=library_window)
            if label and brand and size:
                save_inventory_to_db(file_path, label, brand, size)

    def capture_image():
        if not check_case_table_exists():
            messagebox.showerror("Error", "No case table exists. Please create or load a case first.")
            return

        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            image_path = f"captured_{len(load_inventory_from_db())}.jpg"
            cv2.imwrite(image_path, frame)
            label = simpledialog.askstring("Label Image", "Enter the label for this image:", parent=library_window)
            if label:
                save_inventory_to_db(image_path, label, "Captured Brand", "Captured Size")
        else:
            messagebox.showerror("Error", "Failed to capture image from camera.")
        cap.release()

    def view_uploaded_images():
        if not check_case_table_exists():
            messagebox.showerror("Error", "No case table exists. Please create or load a case first.")
            return

        image_inventory = load_inventory_from_db()
        
        images_window = Toplevel(library_window)
        images_window.title("Uploaded Images")
        images_window.geometry("800x800")

        canvas = Canvas(images_window)
        scrollbar = Scrollbar(images_window, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", on_frame_configure)

        for image_data in image_inventory:
            image_id, file_path, label, brand, size = image_data
            image_frame = Frame(scrollable_frame)
            image_frame.pack(fill='x', padx=5, pady=5)

            img = Image.open(file_path)
            img.thumbnail((300, 300), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            img_label = Label(image_frame, image=img)
            img_label.image = img
            img_label.pack(side="left")

            formatted_label = f"{label} - {brand} - Size: {size}"
            Label(image_frame, text=formatted_label).pack(side="left")

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    upload_btn = Button(library_window, text="Upload Image", command=upload_image)
    upload_btn.pack(pady=10)
    
    capture_btn = Button(library_window, text="Capture Image", command=capture_image)
    capture_btn.pack(pady=10)

    view_images_btn = Button(library_window, text="View Uploaded Images", command=view_uploaded_images)
    view_images_btn.pack(pady=10)

def open_library_window_safe(root):
    global library_window_open
    if not library_window_open:
        library_window_open = True
        open_library_window(root)
    else:
        messagebox.showinfo("Info", "The library window is already open.")

def check_case_table_exists():
    from utils.file_utils import current_case_table
    return current_case_table is not None
