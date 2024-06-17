import subprocess
import signal
import sys
import os

import customtkinter
from cryptography.fernet import Fernet
from PIL import Image

class EntryForm(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        customtkinter.set_default_color_theme("blue")
        customtkinter.set_appearance_mode("dark")

        self.protocol("WM_DELETE_WINDOW", self.on_exit) # uses built in window manager to detect a close event then call the closing function
        signal.signal(signal.SIGINT, self.on_exit) # from the signal lib - signal.SIGINT is when an interupt is detected, so either ctrl + c or closing button
        #signal.signal(signal.SIGCHLD, self.on_exit) #sigchild is sent to the parent process when a child process terminates, specifies that the on_exit should get called
        
        self.geometry("680x400")
        self.title("RascalShell: Admin Portal")
        self.resizable(False, False)

        IMAGE_PATH = 'RLogo.jpg'
        IMAGE_WIDTH = 400
        IMAGE_HEIGHT = 400

        self.image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(IMAGE_PATH)), size=(IMAGE_WIDTH, IMAGE_HEIGHT))
        self.label = customtkinter.CTkLabel(self, image=self.image, text='')
        self.label.grid(row=0, column=0)

        self.logo_frame = customtkinter.CTkFrame(self, fg_color="#F5F5F5", height=20, corner_radius=10, border_width=4, border_color="#0963a7")
        self.logo_frame.grid(row=0, column=1, padx=25, pady=55)

        self.title = customtkinter.CTkLabel(self.logo_frame, text="RascalShell: Admin Portal", font=("", 16, "bold"), text_color="#2C3E50")
        self.title.grid(row=0, column=0, sticky="nsew", pady=5, padx=10)

        self.sep_line = customtkinter.CTkFrame(self.logo_frame, bg_color="#353535", height=1)
        self.sep_line.grid(row=1, column=0, sticky="nsew", pady=20, padx=10)

        self.usernameBox = customtkinter.CTkEntry(self.logo_frame, placeholder_text="Username...", font=("", 13), placeholder_text_color="black", text_color="black", fg_color="#f3f1f0", height=30, corner_radius=7)
        self.usernameBox.grid(row=2, column=0, sticky="nsew", padx=30)

        self.passwordBox = customtkinter.CTkEntry(self.logo_frame, placeholder_text="Password...", font=("", 13), placeholder_text_color="black", text_color="black", fg_color="#f3f1f0", height=30, corner_radius=7, show="*")
        self.passwordBox.grid(row=3, column=0, sticky="nsew", padx=30, pady=20)

        self.loginButton = customtkinter.CTkButton(self.logo_frame, text="Login", height=40, width=150, font=("", 13, "bold"), corner_radius=9, fg_color="#003a86", hover_color="#000099", command=self.key_event)
        self.loginButton.grid(row=4, column=0, sticky="nsew", pady=20, padx=35)

        self.clientWindow = None

        self.after(100, self.key_event)

    def load_key(self):
        file = open("key.key", "rb")
        key = file.read()
        file.close()
        return key

    def key_event(self):

        self.clientUser = self.usernameBox.get()
        self.clientPass = self.passwordBox.get()

        self.key = self.load_key()
        fer = Fernet(self.key)

        with open("RShellCreds.txt", "r") as f:
            for line in f.readlines(): # read every line in the password file
                data = line.rstrip() # removes any whitespace on the right side
                username, password = data.split("|") # this icon is where we split the username and the password

                username = fer.decrypt(username.encode()).decode()
                password = fer.decrypt(password.encode()).decode()
                # encrypted by doing fer.encrypt(username.encode()).decode(), the same for the password. then we decrypt the same way :)
    
        if self.clientUser == username and self.clientPass == password:
            
            python_command = sys.executable
            self.destroy()
            try:
                self.run = subprocess.Popen([python_command, 'shell.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            except Exception as e:
                print(f"Error occured {e}")

    def on_exit(self):
        self.destroy() # destroy the window

if __name__ == "__main__":

    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    """
        
    app = EntryForm()
    app.mainloop()
