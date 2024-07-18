import requests

def fetch_url(url):
    try:
        response = requests.get(url)
        print(f"Statut de la réponse : {response.status_code}")
        if response.status_code == 200:
            print("Contenu de la réponse :")
            print(response.text[:500])  # Affiche les 500 premiers caractères du contenu
        else:
            print("Erreur lors de la récupération de l'URL.")
    except requests.RequestException as e:
        print(f"Erreur lors de l'envoi de la requête : {e}")

def main():
    url = input("Entrez l'URL à récupérer : ")
    fetch_url(url)

if __name__ == "__main__":
    main()
