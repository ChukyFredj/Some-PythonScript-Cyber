import subprocess

# Définition des informations de connexion
user = 'root'  # Nom d'utilisateur pour se connecter à MySQL
password = 'votre_mot_de_passe'  # Mot de passe de l'utilisateur
database = 'exemple_db'  # Nom de la base de données

# Commande pour exécuter une requête SQL
command = f"mysql -u {user} -p{password} -D {database} -e 'SELECT * FROM utilisateurs;'"

# Exécution de la commande via subprocess
result = subprocess.run(command, shell=True, capture_output=True, text=True)

if result.returncode == 0:
    print("Résultat de la requête :")
    print(result.stdout)
else:
    print("Erreur lors de l'exécution de la requête :")
    print(result.stderr)