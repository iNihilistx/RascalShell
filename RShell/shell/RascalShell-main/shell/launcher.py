import subprocess

def main():
    # run the updater first
    subprocess.run(["python", "update_checker.py"])
    subprocess.run(["python", "portal.py"])

if __name__ == "__main__":
    main()