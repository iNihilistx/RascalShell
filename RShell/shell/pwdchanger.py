from cryptography.fernet import Fernet

def main():
    # Provided key
    key = b'U5F-r58nlYpcZVWshm1bHnNJylzToXzuVPCxaeRiN9o='
    
    # Create Fernet instance with the key
    fer = Fernet(key)

    # Get username and password from user
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Encrypt username and password using Fernet
    encrypted_username = fer.encrypt(username.encode()).decode()
    encrypted_password = fer.encrypt(password.encode()).decode()

    # Write encrypted credentials into the creds file
    with open("RShellCreds.txt", "w") as f:
        f.write(f"{encrypted_username}|{encrypted_password}")

    print("Encrypted credentials have been written to RShellCreds.txt.")

if __name__ == "__main__":
    main()
