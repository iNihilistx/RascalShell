import os
import sys
import requests
import zipfile
import subprocess

# Function to download and extract the latest repository archive from GitHub
def download_extract_latest_release(owner, repo):
    url = f"https://github.com/{owner}/{repo}/archive/main.zip"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes

    # Save the zip file to a temporary location
    with open('latest_release.zip', 'wb') as file:
        file.write(response.content)

    # Extract the contents of the zip file
    with zipfile.ZipFile('latest_release.zip', 'r') as zip_ref:
        zip_ref.extractall()

    # Remove the temporary zip file
    os.remove('latest_release.zip')

# Function to fetch the local commit hash from file
def get_local_commit_hash():
    try:
        with open('latest_commit.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

# Function to update the local commit hash in file
def update_local_commit_hash(commit_hash):
    with open('latest_commit.txt', 'w') as file:
        file.write(commit_hash)

# Function to check for updates logic
def check_for_updates_logic(owner, repo):

    latest_commit = get_latest_commit_hash(owner, repo)
    local_commit = get_local_commit_hash()

    if latest_commit and latest_commit != local_commit:
        print("Changes detected in the repository. Updating files...")

        try:
            download_extract_latest_release(owner, repo)
        except Exception as e:
            print(f"Error downloading or extracting repository archive: {e}")
            return False

        update_local_commit_hash(latest_commit)
        return True
    else:
        print("No changes detected in the repository.")
        return False

# Function to fetch the latest commit hash from GitHub repository
def get_latest_commit_hash(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes
    commits = response.json()
    if commits:
        return commits[0]['sha']  # Return the SHA of the latest commit
    else:
        return None

# Main function to run the update check and launch the application
def main():
    owner = "iNihilistx"  # GitHub owner or organization
    repo = "RascalShell"  # GitHub repository name

    try:
        while True:
            if check_for_updates_logic(owner, repo):
                print("Update applied. Restarting application...")
                # Launch the main application after the update check
                subprocess.run(["python", "portal.py"])  # Adjust as per your launcher script
                sys.exit(0)
            else:
                print("No update required. Launching application...")
                # Launch the main application directly if no updates were applied
                subprocess.run(["python", "portal.py"])  # Adjust as per your launcher script
                sys.exit(0)
                


    except Exception as e:
        print(f"Error checking for updates: {e}")
        print("Launching application without update...")

if __name__ == "__main__":
    main()
