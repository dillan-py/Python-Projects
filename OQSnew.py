import oqs
import os
import sys
import time
import csv
import psutil  # For memory usage

# Define the Kyber algorithm variant
KYBER_ALG = "Kyber1024"

def generate_keys():
    """Generate a Kyber key pair (public and secret keys)."""
    kem = oqs.KeyEncapsulation(KYBER_ALG)
    public_key = kem.generate_keypair()
    secret_key = kem.export_secret_key()  # Store secret key
    return public_key, secret_key, kem

def encrypt_file(input_file, public_key):
    """Encrypt a file using the public key and calculate metrics."""
    kem = oqs.KeyEncapsulation(KYBER_ALG)
    kem.generate_keypair()  # Necessary for proper initialization
    
    # Start timer for encapsulation
    start_encap_time = time.time()
    shared_secret, ciphertext = kem.encap_secret(public_key)  # Encrypt using public key
    end_encap_time = time.time()
    encapsulation_time = end_encap_time - start_encap_time

    # Read the file contents
    with open(input_file, "rb") as f:
        file_data = f.read()
    
    # Start timer for encryption
    start_encryption_time = time.time()
    encrypted_data = bytes([b ^ shared_secret[i % len(shared_secret)] for i, b in enumerate(file_data)])
    end_encryption_time = time.time()
    encryption_time = end_encryption_time - start_encryption_time

    # Save the encrypted file (ciphertext + encrypted data)
    enc_file = input_file + ".enc"
    with open(enc_file, "wb") as f:
        f.write(len(ciphertext).to_bytes(4, "big") + ciphertext + encrypted_data)  # Store length + ciphertext + encrypted data

    # Calculate memory usage
    memory_usage = psutil.Process(os.getpid()).memory_info().rss / (1024 ** 2)  # Memory in MB

    print(f"File encrypted: {enc_file}")
    return ciphertext, enc_file, encapsulation_time, encryption_time, memory_usage

def decrypt_file(encrypted_file, secret_key, kem):
    """Decrypt a file using the secret key and calculate metrics."""
    with open(encrypted_file, "rb") as f:
        data = f.read()

    # Extract the ciphertext length (first 4 bytes)
    ciphertext_len = int.from_bytes(data[:4], "big")
    ciphertext = data[4:4 + ciphertext_len]
    encrypted_data = data[4 + ciphertext_len:]
    
    # Start timer for decapsulation
    start_decap_time = time.time()
    shared_secret = kem.decap_secret(ciphertext)
    end_decap_time = time.time()
    decapsulation_time = end_decap_time - start_decap_time

    # Start timer for decryption
    start_decryption_time = time.time()
    decrypted_data = bytes([b ^ shared_secret[i % len(shared_secret)] for i, b in enumerate(encrypted_data)])
    end_decryption_time = time.time()
    decryption_time = end_decryption_time - start_decryption_time

    # Save the decrypted file
    dec_file = encrypted_file.replace(".enc", ".dec")
    with open(dec_file, "wb") as f:
        f.write(decrypted_data)

    print(f"File decrypted: {dec_file}")
    return decapsulation_time, decryption_time

def process_csv(csv_file):
    """Process files specified in a CSV file."""
    try:
        # Attempt to open the CSV file with utf-8 encoding
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                input_file = row["input_file"]
                if not os.path.exists(input_file):
                    print(f"Error: File {input_file} not found.")
                    continue

                # Generate keys (returns kem instance as well)
                public_key, secret_key, kem = generate_keys()

                # Encrypt file
                ciphertext, enc_file, encap_time, enc_time, mem_usage = encrypt_file(input_file, public_key)
                print(f"Encapsulation Time: {encap_time} s, Encryption Time: {enc_time} s, Memory Usage: {mem_usage} MB")

                # Decrypt file using the same kem instance
                decap_time, dec_time = decrypt_file(enc_file, secret_key, kem)
                print(f"Decapsulation Time: {decap_time} s, Decryption Time: {dec_time} s")

    except UnicodeDecodeError:
        print("Error: Failed to decode the CSV file in utf-8. Retrying with ISO-8859-1 encoding...")
        with open(csv_file, "r", encoding="ISO-8859-1") as f:
            reader = csv.DictReader(f)
            for row in reader:
                input_file = row["input_file"]
                if not os.path.exists(input_file):
                    print(f"Error: File {input_file} not found.")
                    continue

                # Generate keys (returns kem instance as well)
                public_key, secret_key, kem = generate_keys()

                # Encrypt file
                ciphertext, enc_file, encap_time, enc_time, mem_usage = encrypt_file(input_file, public_key)
                print(f"Encapsulation Time: {encap_time} s, Encryption Time: {encap_time} s, Memory Usage: {mem_usage} MB")

                # Decrypt file using the same kem instance
                decap_time, dec_time = decrypt_file(enc_file, secret_key, kem)
                print(f"Decapsulation Time: {decap_time} s, Decryption Time: {dec_time} s")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 encrypt.py <csv_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    if not os.path.exists(csv_file):
        print("Error: CSV file not found.")
        sys.exit(1)

    process_csv(csv_file)

if __name__ == "__main__":
    main()
