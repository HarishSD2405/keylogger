from cryptography.fernet import Fernet

key = Fernet.generate_key()
file = open("C:\\Users\\Harish\\OneDrive\\College\\cybersecurity-projects\\KEYLOGGER\\cryptography\\encryption_key","wb")
file.write(key)
file.close