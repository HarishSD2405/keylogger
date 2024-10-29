from cryptography.fernet import Fernet
import os

key = "NG2C0jvomx62ldZ3cKdfPl4BKLo1kC5m52VRL20k_Qk="
fernet = Fernet(key)

# Directory paths
base_directory = "C:\\Users\\Harish\\OneDrive\\College\\cybersecurity-projects\\KEYLOGGER\\cryptography\\"
encrypted_folder = base_directory + "encrypted-files\\"
decrypted_folder = base_directory + "decrypted-files\\"

# Iterate over each file in the encrypted folder
for filename in os.listdir(encrypted_folder):
    encrypted_file_path = encrypted_folder + filename
    
    # Read the encrypted data
    with open(encrypted_file_path, 'rb') as file:
        encrypted_data = file.read()

    # Decrypt the data
    decrypted_data = fernet.decrypt(encrypted_data)

    # Define the decrypted file path in the decrypted folder
    decrypted_file_path = decrypted_folder + "dec_" + filename
    
    # Write the decrypted data to the new file
    with open(decrypted_file_path, 'wb') as file:
        file.write(decrypted_data)

print("All files in the 'encrypted files' folder have been decrypted.")