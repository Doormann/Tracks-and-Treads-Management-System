import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from gui.library_gui import open_library_window_safe
from utils.file_utils import check_case_table_exists

class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tracks and Treads Management System")
        self.root.geometry("750x750")

        self.label_text = tk.StringVar()
        self.setup_background()
        self.setup_buttons()

    def setup_background(self):
        background_image_path = r"TTMS2.5.0\assets\track_logo.png"
        try:
            background_image = Image.open(background_image_path)
            background_image = background_image.resize((750, 750), Image.LANCZOS)
            self.background_photo = ImageTk.PhotoImage(background_image)
            background_label = ttk.Label(self.root, image=self.background_photo)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")

    def setup_buttons(self):
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12), borderwidth='4')
        style.map('TButton', foreground=[('active', '!disabled', 'green')], background=[('active', 'black')])

        buttons = [
            ("Create Case Folder", self.create_case_folder_with_dialog),
            ("Load Case Folder", self.load_case_folder),
            ("View Image Library", self.safe_open_library_window),
            ("Inventory Tread Checker", self.match_shoe_print),
        ]

        for text, command in buttons:
            btn = ttk.Button(self.root, text=text, command=command, style='TButton')
            btn.pack(pady=15, padx=10, expand=True)

        probability_label = ttk.Label(self.root, textvariable=self.label_text, background='white')
        probability_label.pack(fill='x', side='bottom')

    def create_case_folder_with_dialog(self):
        from utils.file_utils import create_case_folder_with_dialog
        create_case_folder_with_dialog(self.root)

    def load_case_folder(self):
        from utils.file_utils import load_case_folder
        load_case_folder()

    def match_shoe_print(self):
        from utils.matching_utils import match_shoe_print
        match_shoe_print(self.label_text)

    def safe_open_library_window(self):
        if check_case_table_exists():
            open_library_window_safe(self.root)
        else:
            from tkinter import messagebox
            messagebox.showerror("Error", "No case table exists. Please create or load a case first.")
