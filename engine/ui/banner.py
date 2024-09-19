import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class Banner:
    def __init__(self, app):
        self.app = app

    def setup(self):
        # Blue banner
        self.banner = tk.Frame(self.app.frame, bg='#007acc')
        self.banner.pack(fill=tk.X, padx=10, pady=10)

        # Load home button image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        home_image_path = os.path.join(script_dir, '../../wallpaper/home.png')
        self.home_image = ImageTk.PhotoImage(Image.open(home_image_path).resize((30, 30)))

        # Load lock/unlock button images
        lock_image_path = os.path.join(script_dir, '../../wallpaper/lock.png')
        self.lock_image = ImageTk.PhotoImage(Image.open(lock_image_path).resize((30, 30)))
        unlock_image_path = os.path.join(script_dir, '../../wallpaper/unlock.png')
        self.unlock_image = ImageTk.PhotoImage(Image.open(unlock_image_path).resize((30, 30)))

        # Load settings button image
        settings_image_path = os.path.join(script_dir, '../../wallpaper/settings.png')
        self.settings_image = ImageTk.PhotoImage(Image.open(settings_image_path).resize((30, 30)))

        # Buttons in the blue banner
        button_style = {
            'fg': 'black',
            'bg': '#bf0e09',  # Default background color
            'activebackground': '#ff00ff',  # Hover background color
            'activeforeground': 'black',
            'bd': 0,
            'highlightthickness': 0,
            'font': ('Roman', 12, 'bold')
        }

        self.home_button = tk.Button(self.banner, image=self.home_image, command=self.app.load_table_of_contents, **button_style)
        self.home_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.add_password_button = tk.Button(self.banner, text="Add PW", command=self.app.add_delete_password.add_password, **button_style)
        self.add_password_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.delete_password_button = tk.Button(self.banner, text="Delete PW", command=self.app.add_delete_password.delete_password, **button_style)
        self.delete_password_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.add_category_button = tk.Button(self.banner, text="Add Category", command=self.app.manage_category.add_category, **button_style)
        self.add_category_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.remove_category_button = tk.Button(self.banner, text="Remove Category", command=self.app.manage_category.remove_category, **button_style)
        self.remove_category_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.copy_button = tk.Button(self.banner, text="Copy", command=self.app.add_delete_password.copy_passwords, **button_style)
        self.copy_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.select_button = tk.Button(self.banner, text="Select Mode", command=self.app.toggle_select_mode, **button_style)
        self.select_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.lock_button = tk.Button(self.banner, image=self.lock_image, command=self.app.toggle_copy_mode, borderwidth=0, relief="flat")
        self.lock_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.settings_button = tk.Button(self.banner, image=self.settings_image, command=self.open_settings, borderwidth=0, relief="flat")
        self.settings_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.app.category_label = tk.Label(self.banner, text="", bg='#007acc', fg='white', font=('Roman', 18, 'bold', 'underline'))
        self.app.category_label.pack(side=tk.LEFT, padx=10, pady=10, ipadx=5, ipady=5)

        self.prev_button = tk.Button(self.banner, text="Previous", command=self.app.previous_page, **button_style)
        self.prev_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.page_label = tk.Label(self.banner, text=f"Page {self.app.current_page + 1}", bg='#007acc', fg='white', font=('Arial', 12, 'bold'))
        self.page_label.pack(side=tk.LEFT, padx=10, pady=10)

        self.next_button = tk.Button(self.banner, text="Next", command=self.app.next_page, **button_style)
        self.next_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Setting the background color for other buttons
        for button in [self.add_password_button, self.add_category_button, self.remove_category_button, self.prev_button, self.next_button, self.delete_password_button, self.copy_button, self.select_button]:
            button.config(bg='#bf0e09')

        for button in [self.home_button, self.add_password_button, self.add_category_button, self.remove_category_button, self.prev_button, self.next_button, self.delete_password_button, self.copy_button, self.lock_button, self.settings_button, self.select_button]:
            button.bind("<Enter>", self.on_enter)
            button.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        e.widget['background'] = '#ff00ff'
        e.widget['cursor'] = 'hand2'

    def on_leave(self, e):
        e.widget['background'] = '#bf0e09'
        e.widget['cursor'] = 'arrow'

    def update_page_label(self):
        self.page_label.config(text=f"Page {self.app.current_page + 1} of {self.app.total_pages}")

    def update_lock_icon(self, copy_mode):
        if copy_mode:
            self.lock_button.config(image=self.unlock_image)
        else:
            self.lock_button.config(image=self.lock_image)

    def open_settings(self):
        settings_window = tk.Toplevel(self.app)
        settings_window.title("Settings")
        settings_window.geometry("300x200")

        ignore_lock_unlock_dialogue_var = tk.BooleanVar(value=self.app.ignore_lock_unlock_dialogue)
        ignore_lock_unlock_dialogue_check = tk.Checkbutton(
            settings_window, 
            text="Ignore lock/unlock dialogue", 
            variable=ignore_lock_unlock_dialogue_var
        )
        ignore_lock_unlock_dialogue_check.pack(pady=10)

        def apply_settings():
            self.app.update_ignore_lock_unlock_dialogue(ignore_lock_unlock_dialogue_var.get())
            self.app.save_settings()
            settings_window.destroy()

        def cancel_settings():
            settings_window.destroy()

        apply_button = tk.Button(settings_window, text="Apply + Exit", command=apply_settings)
        apply_button.pack(pady=5)

        cancel_button = tk.Button(settings_window, text="Cancel", command=cancel_settings)
        cancel_button.pack(pady=5)