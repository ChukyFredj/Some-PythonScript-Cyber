import tempfile

# Création d'un fichier temporaire
with tempfile.NamedTemporaryFile(mode='w+t', delete=True) as tmpfile:
    print(f"Nom du fichier temporaire: {tmpfile.name}")
    
    tmpfile.write("Hello, world!\nThis is a temporary file.")
    
    tmpfile.seek(0)
    
    content = tmpfile.read()
    print("Contenu du fichier temporaire :")
    print(content)


print("Le fichier temporaire a été supprimé.")
