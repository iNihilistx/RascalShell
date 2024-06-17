import subprocess
import os

def main():
    subprocess.run(["python", "update_checker.py"])
    # Change directory to where portal.py is located after the update
    portal_dir = os.path.join('shell', 'RascalShell-main', 'shell')
    os.chdir(portal_dir)

    print(f"Current working directory: {os.getcwd()}")  # Verify the current directory

    # Run portal.py
    subprocess.run(["python", "portal.py"])

if __name__ == "__main__":
    main()
