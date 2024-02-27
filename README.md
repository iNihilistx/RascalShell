<div align="center">
  <img src=https://github.com/iNihilistx/ReverseShellGUI/assets/64751372/bd56664a-d76f-4de5-91b4-dc86ddb18498 title="Logo Generated using Bing AI" width=350 height=300/>
  <h1><b>RascalShell</b></h1>
</div>

## 🖥️ About the Project

<div>
  <p1>
  Developed for my Computer Science degrees Final Year Project. This reverse shell does something unique by implementing a command center through the use of the customtkinter library. Packaged along with this shell are two client projects. CLI - Allows for the standard reverse shell functionality for executing commands and flying under the radar. GUI - Allows the shell to function more like a remote machine handler. This project uses a mixture of GUI development, encryption and socket programming using the OOP paradigm.


## ❗ Disclaimer:

This reverse shell software is intended for educational and learning purposes only. By accessing and using this software, you agree that:

1. You understand the potential risks and consequences associated with running and executing code from untrusted sources.

2. You will only use this software in environments where you have proper authorization and legal permission to do so. Unauthorized or unlawful use of this software is strictly prohibited.

3. The author of this software takes no responsibility for any misuse, damage, or illegal activities conducted using this software. 

4. You acknowledge that this software may be used to access systems and resources without proper authorization, which may violate applicable laws and regulations. It is your responsibility to ensure compliance with all relevant laws and ethical standards.

5. You agree to use this software at your own risk. The author shall not be liable for any direct, indirect, incidental, special, or consequential damages arising from the use of this software.

6. This software is provided "as is," without warranty of any kind, express or implied. The author makes no representations or warranties regarding the accuracy, reliability, or completeness of the software.

By using this software, you acknowledge that you have read, understood, and agreed to the terms and conditions outlined in this disclaimer. If you do not agree with these terms, you are not authorized to use this software.


## 🔎 Features

* Secure communication between host and intended target through use of socket programming
* fully python, with use of libraries
* Graphical User Interface (GUI)
* Network indicator (shell application) - informs you of network speed and status
* Encrypted login (shell application)
* User friendly applications with secure login and connection
* Custom command implementation ~ Pressing the help button on the bottom of the right panel will display the commands
* Unsecure command blockage (commands that alter the flow of the application or deemed dangerous are within a blocked array)


## 📖 Getting Started

### Prerequisites

- Python 3.x
- libraries:
  - login:
    - subprocess, customtkinter, cryptography Fernet, signal
  - shell:
    - socket, subprocess, threading, tkinter, customtkinter
  - image receiver:
      - socket, pyautogui, io
  - client:
    - socket, subprocess, customtkinter, os
  - image_sender:
    - socket, io, pillow
- stable internet connection
### Installation

1. Clone the repository: `git clone https://github.com/iNihilistx/ReverseShellGUI.git`
2. unzip the folder
3. follow below steps to create listener and establish connection

### Usage

#### Host(shell):
1. Navigate to the project directory: `example: cd app/ReverseShellGUI`
2. Open terminal in directory
3. Start the host using the command: `python3 portal.py` - `python portal.py`
<img src="https://github.com/iNihilistx/ReverseShellGUI/assets/64751372/c84a10c9-612a-4778-8a73-8fd10d7dbcdd" width=550 height=350/>
<img src="https://github.com/iNihilistx/ReverseShellGUI/assets/64751372/a6835899-4a1f-4a33-a791-4fb8c0f0296d"/>
<img src="https://github.com/iNihilistx/ReverseShellGUI/assets/64751372/286c264e-24b1-409e-9671-646f0d23ac9d"/>
<img src="https://github.com/iNihilistx/ReverseShellGUI/assets/64751372/afa9f543-92ac-408e-8957-7a399f457ca0"/>



#### Client CLI:
1. Navigate to the project directory: `example: cd app/ReverseShellGUI`
2. Open terminal in directory
3. Start the client using the command: `python3 client-cli.py`

#### Client GUI:
1. Navigate to the project directory: `example: cd app/ReverseShellGUI`
2. Open terminal in directory
3. start the client using the command `python3 portal.py` - `python portal.py`
5. After entering server details (IP and PORT). The window will redirect you to the connected page where you can see incoming an outbound commands
<img src="https://github.com/iNihilistx/ReverseShellGUI/assets/64751372/b7ee5f7f-4900-4b14-a1ab-219446712e0d" width=550 height=350>
<img src="https://github.com/iNihilistx/ReverseShellGUI/assets/64751372/549d8198-6950-45a9-a0a3-5a96c78c3fd7" width=550 height=350>


## Tools Used

<div>
  <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" title="Python" width="40" height="40"/>
  <img src="https://github.com/devicons/devicon/blob/master/icons/vscode/vscode-original-wordmark.svg" title="Vscode" width="40" height="40"/>
  <img src="https://github.com/devicons/devicon/blob/master/icons/unix/unix-original.svg" title="Vscode" width="40" height="40"/>
  <img src="https://github.com/devicons/devicon/blob/master/icons/windows8/windows8-original.svg" title="Vscode" width="40" height="40"/> 
  <img src="https://github.com/garrett/Tux/blob/main/tux-large.png" title="Linux" width=40 height="40"/>
  <img src="https://raw.githubusercontent.com/iiiypuk/rpi-icon/master/raspberry-pi-logo_resized_256.png" title="Raspberry Pi" width="40" height="40"/> 
  <img src="https://github.com/devicons/devicon/blob/master/icons/git/git-original.svg" title="Git" width="40" height="40"/>
</div>
