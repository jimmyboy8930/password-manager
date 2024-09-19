# Password Manager

**Author:**  
- James Frederick

---

## Overview

This project is a simple password manager built with Python and SQLite. It allows you to securely store and manage passwords, organized by categories. The password data is stored locally in an SQLite database. The manager includes functionalities for adding, retrieving, and deleting passwords and categories.

The Python code is using a SQL Database.

- Work in progress some of the features that once worked, no longer work, especially if I'm going to encrypt everything. But everything conceptually works, just don't store your passwords here yet.

---

## Features

- Store passwords associated with service names and emails.
- Organize passwords into categories.
- Add, retrieve, and delete both passwords and categories.
- Automatically sets up the necessary directories and initializes the database on the first run.
- Settings
- Built in copy button

---

## Usage

### Setup
1. Clone or download this repository.
2. Run the `main.py` script to initialize the database and create the necessary directory structure.

On the first run, the script will:
- Create a `/data` directory.
- Set up the SQLite database (`passwords.db`) with tables for categories and passwords.

### Functions

The following core functions are available in the `main.py` script:

1. **Setup Functions**:
   - `ensure_directories()`: Creates the `/data` directory where the database will be stored if it doesn't already exist.
   - `setup_database()`: Initializes the SQLite database and creates the necessary tables.

2. **Category Management**:
   - `insert_category(name)`: Adds a new category to organize passwords.
   - `delete_category(category_id)`: Deletes a category and all associated passwords.
   - `get_categories()`: Retrieves all categories.

3. **Password Management**:
   - `insert_password(service_name, email, password, category_id)`: Adds a password associated with a service and email under a specific category.
   - `get_passwords(category_id)`: Retrieves all passwords in a specific category.
   - `delete_password_from_db(service_name, email, category_id)`: Deletes a password from a specific category.

### Example Usage

1. **Inserting a Category**:
   insert_category('Social Media')
2. **Inserting a Password**: insert_password('Facebook', 'user@example.com', 'mypassword', 1)  # Assuming category ID 1
3. **Get a Passwords**: passwords = get_passwords(1)  # Retrieves passwords in category ID

---
## Version 2.0

- This is not encrypted, so make sure your on an encrypted os, until I fix this.
