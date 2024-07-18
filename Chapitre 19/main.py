import bcrypt

def load_passwords(file_path):
    passwords = []
    with open(file_path, "r") as f:
        for line in f:
            login, pwd = line.strip().split(":")
            passwords.append((login, pwd))
    return passwords

def brute_force_password(hashed_password, wordlist):
    with open(wordlist, "r") as f:
        for word in f:
            word = word.strip()
            print(f"Trying: {word}")
            if bcrypt.checkpw(word.encode('utf-8'), hashed_password.encode('utf-8')):
                return word
    return None

if __name__ == "__main__":
    # Charger la liste des mots de passe
    passwords = load_passwords("logins_passwords.txt")
    
    # Hashed password à déchiffrer
    for login, hashed_password in passwords:
        if login == "kali":  # Utilisateur avec le mot de passe chiffré
            print(f"Essai de déchiffrement du mot de passe pour {login}...")
            found_password = brute_force_password(hashed_password, "wordlist.txt")
            if found_password:
                print(f"Mot de passe trouvé : {found_password}")
                break
            else:
                print("Mot de passe non trouvé.")
