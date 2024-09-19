from tkinter import simpledialog, messagebox
import tkinter as tk

from database import delete_category, get_categories, get_passwords, insert_category

class ManageCategory:
    def __init__(self, app):
        self.app = app

    def display_table_of_contents(self):
        self.app.current_category_id = None
        self.app.current_category_name = None
        self.app.category_label.config(text="Table of Contents")
        self.app.category_tree.delete(*self.app.category_tree.get_children())
        self.app.category_tree['columns'] = ('Category', 'Page')
        self.app.category_tree.column('#0', width=0, stretch=tk.NO)
        self.app.category_tree.column('Category', anchor=tk.CENTER, width=300)
        self.app.category_tree.column('Page', anchor=tk.CENTER, width=100)
        self.app.category_tree.heading('#0', text='', anchor=tk.CENTER)
        self.app.category_tree.heading('Category', text='Category', anchor=tk.CENTER)
        self.app.category_tree.heading('Page', text='Page', anchor=tk.CENTER)

        for idx, category in enumerate(self.app.categories):
            page_number = idx + 2  # Page 1 is the table of contents, so categories start at page 2
            self.app.category_tree.insert("", "end", iid=category[0], text=category[0], values=(category[1], page_number))

        self.app.update_page_label()

    def display_category(self):
        self.app.category_label.config(text=self.app.current_category_name)
        self.app.category_tree.delete(*self.app.category_tree.get_children())
        self.app.category_tree['columns'] = ('Multi', 'Name', 'Email', 'Password')
        self.app.category_tree.column('#0', width=0, stretch=tk.NO)
        self.app.category_tree.column('Multi', anchor=tk.W, width=50)  # Adjusted width for Multi column
        self.app.category_tree.column('Name', anchor=tk.CENTER, width=120)
        self.app.category_tree.column('Email', anchor=tk.CENTER, width=200)
        self.app.category_tree.column('Password', anchor=tk.CENTER, width=200)
        self.app.category_tree.heading('#0', text='', anchor=tk.W)
        self.app.category_tree.heading('Multi', text='Multi', anchor=tk.W)
        self.app.category_tree.heading('Name', text='Name', anchor=tk.CENTER)
        self.app.category_tree.heading('Email', text='Email', anchor=tk.CENTER)
        self.app.category_tree.heading('Password', text='Password', anchor=tk.CENTER)

        if self.app.current_category_id:
            passwords = get_passwords(self.app.current_category_id)
            for pwd in passwords:
                self.app.category_tree.insert("", "end", text="", values=("", pwd[0], pwd[1], pwd[2]))
            self.app.update_page_label()

    def add_category(self):
        category_name = simpledialog.askstring("Category", "Enter the category name:")
        if category_name and category_name[0].isalpha():
            insert_category(category_name)
            self.app.load_data()  # Reload categories to refresh the view
        else:
            messagebox.showerror("Error", "Category name must start with a letter.")

    def remove_category(self):
        category_name = simpledialog.askstring("Remove Category", "Enter the category name to remove:")
        if category_name:
            categories = get_categories()
            for cat in categories:
                if cat[1] == category_name:
                    delete_category(cat[0])
                    self.app.load_data()
                    messagebox.showinfo("Success", "Category removed successfully.")
                    return
            messagebox.showerror("Error", "Category not found.")
        else:
            messagebox.showerror("Error", "Category name cannot be empty.")