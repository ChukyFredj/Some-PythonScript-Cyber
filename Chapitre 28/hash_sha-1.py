import hashlib

def hash_password(password):
    """Hash a password using SHA-1"""
    sha1 = hashlib.sha1()
    sha1.update(password.encode('utf-8'))
    return sha1.hexdigest()

password = "kali"
hashed_password = hash_password(password)
print(f"SHA-1 hashed password for '{password}': {hashed_password}")
