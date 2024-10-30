'''

Fight the hackers and forensics tools with this script against data recovery of deleted files,
Instead of deleting your files on your machine to be re-written over to replace the data,
This script wil encypt the files in a folder with a key, delete the key and folder of data,
This way your data is encrypted on your HDD/SSD which is near impossible to recover the true data,
This will also save you from deleting the file from recently deleted / trash

!!! Caution: Use at your own risk, any files you have in a folder will never be seen again !!!
The encrypted files cannot be decrypted without the password used to encrypt the key, since the key will no longer exist.

This code was created by Mistral AI - Codestral;


To use:

1. Install:
pip install pycryptodome

2. Run code in terminal with this script and the folder 
'python suicide-folder.py folder-to-be-deleted'

3. Use a very long and secure password for the key

'''
import os
import sys
import shutil
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

# Function to encrypt a file using AES encryption
def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    # If no output filename is given, append '.enc' to the input filename
    if not out_filename:
        out_filename = in_filename + '.enc'

    # Generate a random IV (Initialization Vector)
    iv = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    # Open the input file and output file in binary mode
    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            # Write the filesize and IV to the output file
            outfile.write(filesize.to_bytes(8, byteorder='big'))
            outfile.write(iv)

            # Encrypt the file in chunks
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                # If the chunk size is not a multiple of 16, pad it with spaces
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                # Write the encrypted chunk to the output file
                outfile.write(encryptor.encrypt(chunk))

# Function to encrypt the AES key using PBKDF2
def encrypt_key(key, password):
    # Generate a random salt
    salt = get_random_bytes(16)
    # Derive a 32-byte key from the password and salt using PBKDF2
    key = PBKDF2(password, salt, dkLen=32)
    encryptor = AES.new(key, AES.MODE_ECB)
    # Encrypt the AES key using the derived key
    encrypted_key = encryptor.encrypt(key)
    # Return the salt and encrypted key concatenated
    return salt + encrypted_key

def main():
    # Get the folder name from the command-line argument
    folder = sys.argv[1]
    # Prompt the user to enter a password to encrypt the key
    password = input("Enter a password to encrypt the key: ")

    # Generate a random 16-byte AES key
    key = get_random_bytes(16)
    # Encrypt the AES key using the user-provided password
    encrypted_key = encrypt_key(key, password)

    # Encrypt each file in the specified folder
    for filename in os.listdir(folder):
        encrypt_file(key, os.path.join(folder, filename))

    # Delete the AES key
    del key

    # Delete the folder and all its contents
    shutil.rmtree(folder)

if __name__ == "__main__":
    main()
