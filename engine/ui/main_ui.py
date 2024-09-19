import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from PIL import Image, ImageTk
from database import get_categories
from ui.add_delete_password import AddDeletePassword
from ui.manage_category import ManageCategory
from ui.banner import Banner
import os
import time
import json

class PasswordManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager")
        self.geometry("800x600")
        self.attributes('-fullscreen', False)
        self.current_page = 0  # Start at the table of contents
        self.total_pages = 0
        self.pages = []
        self.categories = []
        self.current_category_id = None  # Initialize current_category_id
        self.current_category_name = None
        self.last_copy_time = 0  # To track the last copy time
        self.copy_mode = False  # To toggle between copy and normal mode
        self.select_mode = False  # To toggle between select mode and normal mode
        self.ignore_lock_unlock_dialogue = False  # For settings
        
        # Initialize these instances before setup_ui is called
        self.add_delete_password = AddDeletePassword(self)
        self.manage_category = ManageCategory(self)
        
        self.setup_ui()
        self.load_data()
        self.load_settings()

    def setup_ui(self):
        # Get the absolute path of the background image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bg_image_path = os.path.join(script_dir, '../../wallpaper/background.jpg')
        
        try:
            image = Image.open(bg_image_path)
            self.bg_image = ImageTk.PhotoImage(image)
            self.bg_label = tk.Label(self, image=self.bg_image)
            self.bg_label.place(relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")

        self.frame = tk.Frame(self, bg='#007acc')
        self.frame.place(relwidth=1, relheight=1, relx=0, rely=0)

        # Setup the banner
        self.banner = Banner(self)
        self.banner.setup()

        # Treeview for displaying categories and passwords
        self.category_tree = ttk.Treeview(self.frame)
        self.category_tree.pack(fill=tk.BOTH, expand=True)
        self.category_tree.bind("<Button-1>", self.on_single_click)
        self.category_tree.bind("<Double-1>", self.on_double_click)

    def on_single_click(self, event):
        if self.current_page == 0:  # Table of Contents page
            selected_item = self.category_tree.selection()
            if not selected_item:
                return

            self.current_category_id = int(self.category_tree.item(selected_item[0], "text"))
            self.current_category_name = self.category_tree.item(selected_item[0], "values")[0]
            self.current_page = self.categories.index((self.current_category_id, self.current_category_name)) + 1
            self.manage_category.display_category()
            self.update_page_label()
        elif self.select_mode:
            self.toggle_select(event)

    def on_double_click(self, event):
        if self.copy_mode:
            region = self.category_tree.identify_region(event.x, event.y)
            if region == "cell":
                selected_item = self.category_tree.selection()
                if selected_item:
                    column = self.category_tree.identify_column(event.x)
                    column_index = int(column[1:]) - 1
                    values = list(self.category_tree.item(selected_item[0], "values"))

                    new_value = simpledialog.askstring("Edit Value", f"Enter new value for {self.category_tree.heading(column)['text']}:",
                                                    initialvalue=values[column_index])
                    if new_value is not None:
                        values[column_index] = new_value
                        self.category_tree.item(selected_item[0], values=values)
                        # Here, you should also update the modified value in the database.

    def toggle_copy_mode(self):
        self.copy_mode = not self.copy_mode
        self.banner.update_lock_icon(self.copy_mode)
        if not self.ignore_lock_unlock_dialogue:
            mode = "enabled" if self.copy_mode else "disabled"
            messagebox.showinfo("Mode Toggled", f"Copy/Edit mode {mode}.")

    def toggle_select_mode(self):
        self.select_mode = not self.select_mode
        mode = "enabled" if self.select_mode else "disabled"
        messagebox.showinfo("Mode Toggled", f"Select mode {mode}.")

    def toggle_select(self, event):
        region = self.category_tree.identify_region(event.x, event.y)
        if region == "cell":
            column = self.category_tree.identify_column(event.x)
            if column == '#1':  # Multi column
                selected_item = self.category_tree.selection()
                if selected_item:
                    current_value = self.category_tree.item(selected_item[0], "values")[0]
                    new_value = "✓" if current_value == "" else ""
                    self.category_tree.set(selected_item[0], column="Multi", value=new_value)

    def load_data(self):
        self.categories = get_categories()
        self.total_pages = len(self.categories) + 1  # +1 for the table of contents
        self.manage_category.display_table_of_contents()

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            if self.current_page == 0:
                self.manage_category.display_table_of_contents()
            else:
                self.load_category_page()
            self.update_page_label()

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            if self.current_page == 0:
                self.manage_category.display_table_of_contents()
            else:
                self.load_category_page()
            self.update_page_label()

    def load_category_page(self):
        self.current_category_id = self.categories[self.current_page - 1][0]
        self.current_category_name = self.categories[self.current_page - 1][1]
        self.manage_category.display_category()

    def update_page_label(self):
        self.banner.update_page_label()

    def save_settings(self):
        settings = {
            "ignore_lock_unlock_dialogue": self.ignore_lock_unlock_dialogue,
            "column_widths": [self.category_tree.column(col)["width"] for col in self.category_tree["columns"]]
        }
        with open("settings.json", "w") as f:
            json.dump(settings, f)

    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)
                self.ignore_lock_unlock_dialogue = settings.get("ignore_lock_unlock_dialogue", False)
                column_widths = settings.get("column_widths", [])
                for col, width in zip(self.category_tree["columns"], column_widths):
                    self.category_tree.column(col, width=width)
        except FileNotFoundError:
            pass

    def update_ignore_lock_unlock_dialogue(self, value):
        self.ignore_lock_unlock_dialogue = value
        self.save_settings()

    def load_table_of_contents(self):
        self.current_page = 0
        self.manage_category.display_table_of_contents()