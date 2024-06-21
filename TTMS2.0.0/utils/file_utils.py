import os
import sqlite3
import sys
from tkinter import messagebox, simpledialog, filedialog

db_file_path = None
current_case_table = None

def set_db_file_path(path):
    global db_file_path
    db_file_path = path

def set_current_case_table(case_name):
    global current_case_table
    current_case_table = f"image_inventory_{case_name.replace(' ', '_')}"

def init_db(path):
    set_db_file_path(path)
    try:
        conn = sqlite3.connect(db_file_path)
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to initialize database: {str(e)}")

def create_case_table(case_name):
    set_current_case_table(case_name)
    try:
        conn = sqlite3.connect(db_file_path)
        cursor = conn.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {current_case_table} (
                id INTEGER PRIMARY KEY,
                file_path TEXT NOT NULL,
                label TEXT NOT NULL,
                brand TEXT NOT NULL,
                size TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        messagebox.showinfo("Info", f"Table for case '{case_name}' created successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create table: {str(e)}")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.normpath(os.path.join(base_path, relative_path))

def save_inventory_to_db(file_path, label, brand, size):
    if current_case_table is None:
        raise ValueError("Current case table is not set.")
    try:
        conn = sqlite3.connect(db_file_path)
        cursor = conn.cursor()
        cursor.execute(f'''
            INSERT INTO {current_case_table} (file_path, label, brand, size)
            VALUES (?, ?, ?, ?)
        ''', (file_path, label, brand, size))
        conn.commit()
        conn.close()
        messagebox.showinfo("Info", "Inventory saved successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save inventory: {str(e)}")

def load_inventory_from_db():
    if current_case_table is None:
        raise ValueError("Current case table is not set.")
    try:
        conn = sqlite3.connect(db_file_path)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {current_case_table}')
        inventory = cursor.fetchall()
        conn.close()
        return inventory
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load inventory: {str(e)}")
        return []

def create_case_folder(case_name):
    new_folder_path = os.path.join(os.getcwd(), case_name)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        messagebox.showinfo("Success", f"Folder '{case_name}' created at {new_folder_path}")
        create_case_table(case_name)
    else:
        messagebox.showerror("Error", "Folder already exists.")

def create_case_folder_with_dialog(root):
    case_name = simpledialog.askstring("Create Case Folder", "Enter the case name:", parent=root)
    if case_name:
        create_case_folder(case_name)

def load_case_folder():
    folder_path = filedialog.askdirectory(title="Select Case Folder")
    if folder_path:
        case_name = os.path.basename(folder_path)
        set_current_case_table(case_name)
        create_case_table(case_name)
        messagebox.showinfo("Info", "Case loaded successfully.")

def check_case_table_exists():
    return current_case_table is not None
