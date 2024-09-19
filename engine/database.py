import sqlite3
import os

def ensure_directories():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, '../data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

def setup_database():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/passwords.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ensure the categories table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    # Ensure the passwords table exists with the correct columns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    ''')

    conn.commit()
    conn.close()

def get_categories():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/passwords.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM categories')
    categories = cursor.fetchall()
    conn.close()
    return categories

def insert_category(name):
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/passwords.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO categories (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()

def delete_category(category_id):
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/passwords.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
    cursor.execute('DELETE FROM passwords WHERE category_id = ?', (category_id,))
    conn.commit()
    conn.close()

def get_passwords(category_id):
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/passwords.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT service_name, email, password FROM passwords WHERE category_id = ?', (category_id,))
    passwords = cursor.fetchall()
    conn.close()
    return passwords

def insert_password(service_name, email, password, category_id):
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/passwords.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO passwords (service_name, email, password, category_id) VALUES (?, ?, ?, ?)', (service_name, email, password, category_id))
    conn.commit()
    conn.close()

def delete_password_from_db(service_name, email, category_id):
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/passwords.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM passwords WHERE service_name = ? AND email = ? AND category_id = ?', (service_name, email, category_id))
    conn.commit()
    conn.close()