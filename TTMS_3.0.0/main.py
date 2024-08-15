import tkinter as tk
from tkinter import filedialog
from utils.file_utils import init_db
from gui.main_gui import MainGUI

def main():
    root = tk.Tk()

    db_file_path = filedialog.askopenfilename(title="Select Database File", filetypes=[("All files", "*.*")])
    if db_file_path:
        init_db(db_file_path)
        app = MainGUI(root)
        root.mainloop()
    else:
        print("No database file selected. Exiting.")

if __name__ == "__main__":
    main()

