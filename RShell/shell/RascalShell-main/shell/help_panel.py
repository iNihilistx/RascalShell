import customtkinter
import signal
import threading
from tkinter import *

class HelperFrame(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        customtkinter.set_default_color_theme("blue")
        customtkinter.set_appearance_mode("dark")
        
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        signal.signal(signal.SIGINT, self.on_exit)

        self.geometry("720x400")
        self.title("RascalShell: Commands Panel")
        self.resizable(False, False)

        self.command_box = customtkinter.CTkTextbox(self, font=("Open Sans", 14), border_width=2, height=380, width=680)
        self.command_box.grid(row=0, column=0, padx=20, sticky="nsew", pady=(10,0))

        threading.Thread(target=self.populate_helpbox, daemon=True).start()

    def populate_helpbox(self):
        with open("commands.txt", "r") as commands:
            content = commands.read()
            self.command_box.insert("end", content)
            self.command_box.configure(state="disabled")

    def on_exit(self):
        self.destroy()

if __name__ == "__main__":

    app = HelperFrame()
    app.mainloop()

