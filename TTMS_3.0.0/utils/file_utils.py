import os
import sqlite3
import sys
from tkinter import messagebox, simpledialog, filedialog, Toplevel, Listbox, Button
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageChops import offset

db_file_path = None
current_case_table = None

def set_db_file_path(path):
    global db_file_path
    db_file_path = path

def set_current_case_table(case_name):
    global current_case_table
    current_case_table = f"{case_name.replace(' ', '_')}"

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
                size TEXT NOT NULL,
                overall_length TEXT NOT NULL,
                overall_width TEXT NOT NULL,
                heel_length TEXT NOT NULL,
                heel_width TEXT NOT NULL
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

def save_inventory_to_db(file_path, label, brand, size, overall_length, overall_width, heel_length, heel_width):
    if current_case_table is None:
        raise ValueError("Current case table is not set.")
    try:
        conn = sqlite3.connect(db_file_path)
        cursor = conn.cursor()
        cursor.execute(f'''
            INSERT INTO {current_case_table} (file_path, label, brand, size, overall_length, overall_width, heel_length, heel_width)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (file_path, label, brand, size, overall_length, overall_width, heel_length, heel_width))
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

def export_data():
    if current_case_table is None:
        messagebox.showwarning("Warning", "No case table selected.")
        return

    output_directory = filedialog.askdirectory(title="Select Output Directory")
    if not output_directory:
        messagebox.showwarning("Warning", "No output directory selected.")
        return

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    try:
        conn = sqlite3.connect(db_file_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {current_case_table}")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            image_id, file_path, label, brand, size, overall_length, overall_width, heel_length, heel_width = row
            texts = [
                f"Label: {label}",
                f"Brand: {brand}",
                f"Size: {size}",
                f"Overall Length: {overall_length}",
                f"Overall Width: {overall_width}",
                f"Heel Length: {heel_length}",
                f"Heel Width: {heel_width}"
            ]

            # Open the image
            image = Image.open(file_path)

            # Resize the image to a uniform size
            uniform_size = (800, 800)
            image = image.resize(uniform_size, Image.LANCZOS)

            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype("arial.ttf", 24)  # Use a larger font size

            # Calculate the starting position for the text at the bottom left
            x, y = 10, image.height - (len(texts) * 30) - 10

            # Overlay text onto the image
            for text in texts:
                # Draw black outline
                for offset in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                    draw.text((x + offset[0], y + offset[1]), text, font=font, fill="black")
                # Draw yellow text
                draw.text((x, y), text, font=font, fill="yellow")
                y += 30  # Move to the next line

            image = image.convert("RGB")

            # Save the modified image to the specified directory
            output_path = os.path.join(output_directory, f"modified_{label}.jpg")
            image.save(output_path)

        messagebox.showinfo("Info", "Data and images saved successfully.")
    except Exception as e:
        print(f"Error exporting data: {str(e)}")
        messagebox.showerror("Error", f"Failed to export data: {str(e)}")

def check_case_table_exists():
    return current_case_table is not None
