import sys
import os

# Add the parent directory of 'engine' to the Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)

from ui.main_ui import PasswordManagerApp

if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()