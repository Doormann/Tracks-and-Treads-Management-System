import os
import sqlite3
import sys
from tkinter import messagebox, simpledialog, filedialog, Toplevel, Listbox, Button
import tkinter as tk

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

def create_case_folder_with_dialog(root):
    case_name = simpledialog.askstring("Create Case Folder", "Enter the case name:", parent=root)
    if case_name:
        create_case_table(case_name)

def load_case_table():

    tables = get_database_tables(db_file_path)
    if not tables:
        messagebox.showinfo("Info", "No tables found in the database.")
        return

    table_selection_window = Toplevel()
    table_selection_window.title("Select Case Table")

    table_listbox = Listbox(table_selection_window, width=80)
    for table in tables:
        table_name = table[0]
        table_listbox.insert(tk.END, table_name)

    table_listbox.pack(padx=10, pady=10)

    def on_select_table():
        selected_index = table_listbox.curselection()
        if selected_index:
            selected_table = table_listbox.get(selected_index)
            global current_case_table
            current_case_table = selected_table
            messagebox.showinfo("Info", f"Table '{selected_table}' loaded successfully.")
            table_selection_window.destroy()  # Close the selection window
        else:
            messagebox.showwarning("Warning", "Please select a table.")

    select_button = Button(table_selection_window, text="Select Table", command=on_select_table)
    select_button.pack(pady=10)

    close_button = Button(table_selection_window, text="Close", command=table_selection_window.destroy)
    close_button.pack(pady=10)

def get_database_tables(db_path):
    """Fetch the list of tables in the database."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        return tables
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch tables: {str(e)}")
        return []

def display_tables_with_paths():
    """Display the current tables with their file path locations."""
    tables = get_database_tables(db_file_path)

    if not tables:
        messagebox.showinfo("Info", "No tables found in the database.")
        return

    tables_window = Toplevel()
    tables_window.title("Current Tables")

    table_listbox = Listbox(tables_window, width=80)
    for table in tables:
        table_name = table[0]
        table_listbox.insert(tk.END, f"{table_name} - Location: {db_file_path}")

    table_listbox.pack(padx=10, pady=10)

    close_button = Button(tables_window, text="Close", command=tables_window.destroy)
    close_button.pack(pady=10)

def check_case_table_exists():
    return current_case_table is not None
