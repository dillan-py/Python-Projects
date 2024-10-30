'''
Version 2:
Encrypts files and overwrites each file's conent with random data before deletion and removes folder structure
In other words
'The files sheds itself so its unformable again'
'''

import os
import sys
import shutil
from cryptography.fernet import Fernet

def generate_key():
    # Generate and save a key for encryption
    key = Fernet.generate_key()
    with open("encryption.key", "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    # Load the saved key
    return open("encryption.key", "rb").read()

def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        file_data = file.read()
    encrypted_data = fernet.encrypt(file_data)
   
    # Write the encrypted file
    with open(file_path + ".enc", "wb") as file:
        file.write(encrypted_data)
   
    # Securely delete original file after encryption
    secure_delete(file_path)

def encrypt_folder(folder_path):
    key = generate_key()
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key)

def secure_delete(file_path, passes=3):
    # Overwrite the file with random data multiple times
    with open(file_path, "ba+") as delfile:
        length = delfile.tell()
    for _ in range(passes):
        with open(file_path, "br+") as delfile:
            delfile.seek(0)
            delfile.write(os.urandom(length))
    os.remove(file_path)

def delete_folder(folder_path):
    # Securely delete all files in the folder and then delete the folder
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for file in files:
            secure_delete(os.path.join(root, file))
        for directory in dirs:
            os.rmdir(os.path.join(root, directory))
    os.rmdir(folder_path)

def delete_key():
    #Securely delete the encryption key file
    if os.path.exists("encryption.key"):
        secure_delete("encryption.key")

if __name__ == "__main__":
    # Get the folder path from the command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <folder_path>")
        sys.exit(1)

    folder_to_encrypt = sys.argv[1]
   
    # Check if folder exists
    if not os.path.isdir(folder_to_encrypt):
        print(f"Error: Folder '{folder_to_encrypt}' does not exist.")
        sys.exit(1)
   
    # Encrypt and delete the folder
    encrypt_folder(folder_to_encrypt)
    delete_folder(folder_to_encrypt)
    delete_key()

    print("Folder encrypted and securely deleted.")
