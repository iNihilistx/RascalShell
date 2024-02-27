import socket
import io
from PIL import Image

def receive_image():
    host = "192.168.0.26"
    port = 8081
    BUFFER_SIZE = 4096

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(1)

        conn, addr = server_socket.accept()

        image_data = b"" # intialises an empty byte object to store received image data

        while True: # continuously receive data from the client in chunks until there is no more data to retrieve
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            image_data += data # append each of the chunks to the earlier declared variable

        image = Image.open(io.BytesIO(image_data)) # allows you to open the received binary data as an image
        image.show()
        image.save('grabbed.png')

if __name__ == "__main__":
    receive_image()
