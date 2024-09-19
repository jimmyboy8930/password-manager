import time
import tkinter as tk
from tkinter import simpledialog, messagebox

class AddDeletePassword:
    def __init__(self, app):
        self.app = app

    def add_password(self):
        category_name = simpledialog.askstring("Category", "Enter the category name:")
        if category_name and category_name in [category[1] for category in self.app.categories]:
            service_name = simpledialog.askstring("Service Name", "Enter the name of the service:")
            if not service_name:
                return

            email_choice = simpledialog.askstring(
                "Email",
                "Enter the email (1-9 for preselected or type your own):\n" +
                "\n".join([f"{i+1}. example{i+1}@example.com" for i in range(9)]),
                parent=None
            )
            if not email_choice:
                return

            try:
                email_index = int(email_choice) - 1
                email = f"example{email_index + 1}@example.com"
            except (ValueError, IndexError):
                email = email_choice

            password = simpledialog.askstring("Password", "Enter the password:")
            if not password:
                return

            self.app.manage_category.insert_password(service_name, email, password, self.app.current_category_id)
            self.app.manage_category.display_category()  # Refresh category to show added password

    def delete_password(self):
        selected_item = self.app.category_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No password selected.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected password(s)?")
        if confirm:
            for item in selected_item:
                values = self.app.category_tree.item(item, "values")
                service_name = values[0]
                email = values[1]
                self.app.manage_category.delete_password_from_db(service_name, email, self.app.current_category_id)
                self.app.category_tree.delete(item)
            messagebox.showinfo("Success", "Password(s) deleted successfully.")

    def copy_passwords(self):
        selected_items = self.app.category_tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "No password(s) selected.")
            return

        copied_data = []
        for item in selected_items:
            values = self.app.category_tree.item(item, "values")
            copied_data.append(f"{values[1]}, {values[2]}, {values[3]}")  # Name, Email, Password

        if copied_data:
            copied_text = "\n".join(copied_data)
            self.app.clipboard_clear()
            self.app.clipboard_append(copied_text)
            current_time = time.time()
            if current_time - self.app.last_copy_time >= 3:  # 3 seconds timer
                self.app.last_copy_time = current_time
                messagebox.showinfo("Copied", "Copied:\n" + copied_text)
