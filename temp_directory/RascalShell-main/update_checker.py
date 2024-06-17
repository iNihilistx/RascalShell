import os
import shutil
import subprocess
import requests
import zipfile
import time

# Function to delete a directory and all its contents
def delete_directory(directory):
    try:
        shutil.rmtree(directory)
    except Exception as e:
        print(f"Error deleting directory {directory}: {e}")

# Function to create a directory if it does not exist
def create_directory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except Exception as e:
        print(f"Error creating directory {directory}: {e}")

# Function to download and extract the latest repository archive from GitHub
def download_extract_latest_release(owner, repo):
    url = f"https://github.com/{owner}/{repo}/archive/main.zip"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes

    # Save the zip file to a temporary location
    temp_dir = 'temp_directory'
    create_directory(temp_dir)  # Create temp directory if it doesn't exist
    zip_file = os.path.join(temp_dir, 'latest_release.zip')

    with open(zip_file, 'wb') as file:
        file.write(response.content)

    # Extract the contents of the zip file
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    # Remove the temporary zip file
    os.remove(zip_file)

    return temp_dir

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
            temp_dir = download_extract_latest_release(owner, repo)
            # Delete the old 'shell' directory and replace with the new one
            delete_directory('shell')
            shutil.move(temp_dir, 'shell')

            # Update local commit hash
            update_local_commit_hash(latest_commit)
            return True
        except Exception as e:
            print(f"Error updating repository: {e}")
            return False
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
        retry_attempts = 3
        retry_delay = 1  # Delay in seconds between retries

        for _ in range(retry_attempts):
            if check_for_updates_logic(owner, repo):
                print("Update applied. Restarting application...")
                # Launch the main application after the update check
                subprocess.run(["python", "shell/RascalShell-main/shell/portal.py"])
                return  # Exit function after successful update and launch
            else:
                print("No update required. Launching application...")
                # Launch the main application directly if no updates were applied
                subprocess.run(["python", "shell/RascalShell-main/shell/portal.py"])
                return  # Exit function after launching application

            time.sleep(retry_delay)  # Wait before retrying

        else:
            print(f"Failed after {retry_attempts} retries. Launching application without update...")

    except Exception as e:
        print(f"Error checking for updates: {e}")
        print("Launching application without update...")

if __name__ == "__main__":
    main()
