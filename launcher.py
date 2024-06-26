import subprocess
import os

def main():
    # Run the update checker script
    subprocess.run(["python", "update_checker.py"])

    # Directory where portal.py should be located after the update
    portal_dir = os.path.join('shell', 'RascalShell-main', 'shell')

    # Change directory to where portal.py is located after the update
    os.chdir(portal_dir)

    # Verify the current working directory (for debugging)
    print(f"Current working directory: {os.getcwd()}")

    # Run portal.py
    subprocess.run(["python", "portal.py"])

if __name__ == "__main__":
    main()
