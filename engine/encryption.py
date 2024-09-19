from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def encrypt_data(key, data):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(key, data):
    fernet = Fernet(key)
    return fernet.decrypt(data.encode()).decode()