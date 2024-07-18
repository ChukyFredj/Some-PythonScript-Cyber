import os
import json
import base64
import hashlib
import secrets
from cryptography.fernet import Fernet, InvalidToken
from getpass import getpass

# Fonction pour générer une clé Fernet à partir d'un mot de passe maître
def generate_key(master_password):
    password = master_password.encode()
    salt = b'salt_'  # Vous pouvez utiliser une méthode plus sophistiquée pour gérer le sel
    kdf = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
    key = base64.urlsafe_b64encode(kdf[:32])
    return key

# Fonction pour générer un mot de passe aléatoire robuste
def generate_password(length=12):
    if length < 8:
        raise ValueError("La longueur minimale pour un mot de passe robuste est de 8 caractères.")
    
    while True:
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        if test_password_strength(password) == "Forte":
            return password

# Fonction pour tester la robustesse d'un mot de passe
def test_password_strength(password):
    if len(password) < 8:
        return "Faible"
    elif not any(char.isdigit() for char in password):
        return "Moyenne"
    elif not any(char.isupper() for char in password):
        return "Moyenne"
    elif not any(char.islower() for char in password):
        return "Moyenne"
    elif not any(char in "!@#$%^&*()" for char in password):
        return "Moyenne"
    else:
        return "Forte"

# Fonction pour chiffrer des données
def encrypt_data(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

# Fonction pour déchiffrer des données
def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    try:
        decrypted_data = fernet.decrypt(encrypted_data).decode()
        return decrypted_data
    except InvalidToken:
        return "Mauvaise clé maître"

# Fonction pour sauvegarder un mot de passe utilisateur
def save_password(username, password, key):
    password_data = {}
    if os.path.exists('vault.json'):
        with open('vault.json', 'r') as file:
            password_data = json.load(file)

    encrypted_password = encrypt_data(password, key)
    password_data[username] = encrypted_password.decode()

    with open('vault.json', 'w') as file:
        json.dump(password_data, file)

# Fonction pour obtenir la liste des mots de passe utilisateurs
def get_passwords(key):
    if not os.path.exists('vault.json'):
        return {}

    with open('vault.json', 'r') as file:
        password_data = json.load(file)

    decrypted_password_data = {}
    for username, encrypted_password in password_data.items():
        decrypted_password = decrypt_data(encrypted_password, key)
        if decrypted_password == "Mauvaise clé maître":
            decrypted_password_data[username] = "Mauvaise clé maître"
        else:
            decrypted_password_data[username] = decrypted_password

    return decrypted_password_data

def main():
    master_password = getpass("Entrez le mot de passe maître : ")
    key = generate_key(master_password)

    while True:
        print("\nOptions :")
        print("1. Sauvegarder un mot de passe")
        print("2. Obtenir la liste des mots de passe")
        print("3. Générer un mot de passe")
        print("4. Tester la robustesse d'un mot de passe")
        print("5. Quitter")
        
        choice = input("Choisissez une option : ")

        if choice == "1":
            username = input("Entrez le nom d'utilisateur : ")
            while True:
                password = getpass("Entrez le mot de passe : ")
                strength = test_password_strength(password)
                if strength == "Forte":
                    break
                else:
                    print(f"Mot de passe trop faible ({strength}). Veuillez entrer un mot de passe plus robuste.")
            save_password(username, password, key)
            print(f"Mot de passe pour {username} sauvegardé.")
        
        elif choice == "2":
            passwords = get_passwords(key)
            for username, password in passwords.items():
                print(f"Utilisateur : {username}, Mot de passe : {password}")
        
        elif choice == "3":
            length = int(input("Entrez la longueur du mot de passe (minimum 8) : "))
            try:
                password = generate_password(length)
                print(f"Mot de passe généré : {password}")
            except ValueError as e:
                print(e)
        
        elif choice == "4":
            password = getpass("Entrez le mot de passe à tester : ")
            strength = test_password_strength(password)
            print(f"Robustesse du mot de passe : {strength}")
        
        elif choice == "5":
            break
        
        else:
            print("Option invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
