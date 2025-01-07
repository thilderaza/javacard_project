from smartcard.System import readers
from datetime import datetime
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from smartcard.System import readers
from applet import SmartCardApplet  
import requests

# Different articles disponible à l'achat
def display_articles():
    articles = {
        1:{"name": "Bouteille d'eau","prix": 1.10},
        2:{"name": "Haribo Dragibus", "prix": 1.40}
    }
    print("Articles")
    for id_art, art in articles.arts():
        print(f"{id_art}. {articles['name']} - ${articles['prix']:.2f}")
        return articles
    

def select_art(articles):
    select_art = []
    total=0.0

    while True:
        try:
            choice = int(input("Entrez le numéro de l'article à ajouter (0 pour terminer) : "))
            if choice == 0:
                break
            if choice in articles:
                item = articles[choice]
                total += item["prix"]
                print(f"Ajouté : {item['name']} (${item['prix']:.2f})")
            else:
                print("Option invalide, veuillez réessayer.")
        except ValueError:
            print("Entrée invalide, veuillez entrer un numéro.")
    
    return total

def send_apdu(data,applet):
    # Récupère la liste des lecteurs disponibles
    r = readers()
    if len(r) > 0:
        print("Lecteurs disponibles: ",r)
    else:
        print("Il n'y a pas de lecteur.")

    reader = r[0]
    connection = reader.createConnection()
    connection.connect()
    print("Vous êtes connecté au lecteur: ",reader)


    #Commande APDU (transmission des données)
    APDU = [0x80, 0x10, 0x00, 0x00, len(data)] + data
    try:
        response,sw1,sw2 = connection.transmit(APDU)

        #sw valeurs retournées par la carte
        # Succès
        if sw1 == 0x90 and sw2 == 0x00:
            print("Transaction réalisé.")

        # Erreur (Du à un problème d'accès(PIN incorrecte/non vérifié, probleme longueur data, ou fichier) )
        else:
            print(f"Erreur : SW1={sw1}, SW2={sw2}")
        response, sw1, sw2 = applet.process_apdu(APDU)
        return response, sw1, sw2
    except Exception as e:
            print("Erreur lors de la transmission APDU :", str(e))
            return None, None, None

# Récupérer l'horodatage signé
def get_signed_timestamp():
    response = requests.get("http://localhost:5000/get_timestamp")
    if response.status_code == 200:
        data = response.json()
        print("Horodatage signé récupéré :", data)
        return data
    else:
        print("Erreur lors de la récupération de l'horodatage :", response.json())
        return None
    
Envoyer la transaction signée au serveur
def send_to_server(transaction, signature, card_public_key):

    response = requests.post("http://localhost:5000/verify_transaction", json={
        "transaction": transaction,
        "signature": signature.hex(),
        "card_public_key": card_public_key.decode('utf-8')
    })
    print("Réponse du serveur :", response.json())

if __name__ == "__main__":
    # instance de l'applet simulée
    applet = SmartCardApplet(pin="1234")

    # Vérification du PIN
    print("\n=== Vérification du PIN ===")
    pin = input("Entrez votre code PIN : ").encode('utf-8')  # Demande le PIN utilisateur
    response, sw1, sw2 = send_apdu(pin, "verify_pin", applet)  # APDU pour vérifier le PIN
    if sw1 == 0x90:
        print("PIN vérifié avec succès.")
    else:
        print("Échec de la vérification du PIN.")
        exit()  # Arrête le programme si le PIN est incorrect

    # Affichage et sélection des articles
    print("\n=== Sélection des articles ===")
    articles = display_articles()  # Affiche les articles disponibles
    total = select_art(articles)  # Permet la sélection et calcule le total

    # Affiche le total de la transaction
    print(f"\nTotal de la transaction : ${total:.2f}")

    #  Récupération de l'horodatage signé depuis le serveur
    print("\n=== Récupération de l'horodatage signé ===")
    timestamp_data = get_signed_timestamp()  # Appel au serveur pour récupérer l'horodatage signé
    if not timestamp_data:
        print("Erreur : Impossible de récupérer l'horodatage signé.")
        exit()

    # Prépare les données de la transaction
    transaction_data = f"total={int(total * 100)}&timestamp={timestamp_data['timestamp']}"
    print(f"Transaction préparée : {transaction_data}")

    # Signature des données de la transaction par la carte
    print("\n=== Signature de la transaction par la carte ===")
    apdu_sign_data = [0x80, 0x10, 0x00, 0x00, len(transaction_data)] + list(transaction_data.encode('utf-8'))
    response, sw1, sw2 = applet.process_apdu(apdu_sign_data)  # Appel à l'applet pour signer
    if sw1 == 0x90:
        print("Transaction signée avec succès.")
    else:
        print("Échec de la signature de la transaction.")
        exit()

    # Envoi de la transaction signée au serveur pour vérification
    print("\n=== Envoi de la transaction signée au serveur ===")
    card_public_key = applet.get_public_key()  # Récupère la clé publique de la carte
    send_to_server(transaction_data, response, card_public_key)  # Envoi au serveur

    print("\n=== Fin de la transaction ===")
