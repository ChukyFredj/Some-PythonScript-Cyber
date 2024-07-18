import hashlib

def hash_password(password):
    """Hash a password using SHA-1"""
    sha1 = hashlib.sha1()
    print(sha1)
    sha1.update(password.encode('utf-8'))
    return sha1.hexdigest()

def load_password_list(filename):
    """Load a list of passwords from a file"""
    with open(filename, 'r') as file:
        passwords = file.read().splitlines()
    return passwords

def crack_password(hashed_password, password_list):
    """Attempt to crack the hashed password using a list of common passwords"""
    for password in password_list:
        if hash_password(password) == hashed_password:
            return password
    return None

if __name__ == "__main__":
    hashed_password = input("Enter the SHA-1 hashed password to crack: ")

    password_list = load_password_list("wordlist.txt")
    print(f"[INFO] Loaded {len(password_list)} passwords from file.")
    cracked_password = crack_password(hashed_password, password_list)

    if cracked_password:
        print(f"Password cracked: {cracked_password}")
    else:
        print("Failed to crack the password.")
