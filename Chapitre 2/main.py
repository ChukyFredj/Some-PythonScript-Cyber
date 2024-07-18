import spur

# Remplacez ces valeurs par les informations de connexion de votre serveur
hostname = "server_address"  # L'adresse du serveur
username = "username"        # Votre nom d'utilisateur sur le serveur
password = "password"        # Votre mot de passe

shell = spur.SshShell(
    hostname=hostname,
    username=username,
    password=password,
    missing_host_key=spur.ssh.MissingHostKey.accept
)

with shell:
    result = shell.run(["echo", "Hello, SSH!"])
    print(result.output.decode())  # Affiche la sortie de la commande
