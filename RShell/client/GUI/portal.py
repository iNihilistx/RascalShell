import subprocess
import customtkinter
from PIL import Image, ImageTk
import signal
from cryptography.fernet import Fernet
import os

class clientLogin(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.protocol(signal.SIGINT, self.on_exit)

        self.geometry("680x400")
        self.title("Rascal shell Client Portal")
        self.resizable(False, False)
        
        IMAGE_PATH = 'background.jpg'
        IMAGE_WIDTH = 370
        IMAGE_HEIGHT = 400
        
        self.image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(IMAGE_PATH)), size=(IMAGE_WIDTH, IMAGE_HEIGHT))
        self.label = customtkinter.CTkLabel(self, image=self.image, text='')
        self.label.grid(row=0, column=0)
        
        self.logo_frame = customtkinter.CTkFrame(self, fg_color='#F5F5F5', height=20, corner_radius=10, border_width=4, border_color="#CCCCCC")
        self.logo_frame.grid(row=0, column=1, padx=25, pady=55)
        
        self.title = customtkinter.CTkLabel(self.logo_frame, text="RascalShell: Client Portal", font=("", 16, "bold"), text_color="#2C3E50")
        self.title.grid(row=0, column=0, sticky="nsew", pady=5, padx=10)
        
        self.sep_line = customtkinter.CTkFrame(self.logo_frame, bg_color="#353535", height=1)
        self.sep_line.grid(row=1, column=0, sticky="nsew", padx=30, pady=20)
        
        self.server_ip_address = customtkinter.CTkEntry(self.logo_frame, placeholder_text="IP Address...", font=("", 14), placeholder_text_color="black", text_color="black", fg_color="#f3f1f0", height=30, corner_radius=7)
        self.server_ip_address.grid(row=2, column=0, sticky="nsew", padx=30)
        
        self.server_port = customtkinter.CTkEntry(self.logo_frame, placeholder_text="Port Number...", font=("", 14), placeholder_text_color="black", text_color="black", fg_color="#f3f1f0", height=30, corner_radius=7)
        self.server_port.grid(row=3, column=0, sticky="nsew", padx=30, pady=20)
        
        self.connect_button = customtkinter.CTkButton(self.logo_frame, text="Connect", height=40, width=150, font=("", 14, "bold"), corner_radius=9, fg_color="#AE0BE7", hover_color="#C12DF5", command=self.connect_window)
        self.connect_button.grid(row=4, column=0, sticky="nsew", padx=35, pady=20)
        
        self.clientWindow = None

    def load_key(self):
        file = open("key.key", "rb")
        key = file.read()
        file.close()
        return key
    
    def encrypt_server_details(self, server_ip, server_port):
        key = self.load_key()
        cipher = Fernet(key)
        encrypted_data = cipher.encrypt(f"{server_ip}|{server_port}".encode())

        with open("server.txt", "wb") as server_details:
            server_details.write(encrypted_data)

    def connect_window(self):
        self.server_ip = self.server_ip_address.get()
        self.server_port = int(self.server_port.get())

        self.encrypt_server_details(self.server_ip, self.server_port)

        if self.clientWindow is None or not self.clientWindow.winfo_exists():
            self.destroy()
            self.run = subprocess.Popen(['python', 'client.py'])

    def on_exit(self):
        self.destroy()

if __name__ == "__main__":
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    """
    app = clientLogin()
    app.mainloop()