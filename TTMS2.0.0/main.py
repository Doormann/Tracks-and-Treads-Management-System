import tkinter as tk
import os
from tkinter import filedialog
from utils.file_utils import init_db
from gui.main_gui import MainGUI

def main():
    root = tk.Tk()
    
    db_directory = filedialog.askdirectory(title="Select Directory for Database")
    if db_directory:
        db_file_path = os.path.join(db_directory, 'inventory.db')
        init_db(db_file_path)
        app = MainGUI(root)
        root.mainloop()
    else:
        print("No directory selected for database. Exiting.")

if __name__ == "__main__":
    main()
