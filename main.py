from applet import SmartCardApplet
from terminal_app import send_apdu, display_articles, select_art, get_signed_timestamp, send_to_server

if __name__ == "__main__":
    # simulated applet instance
    applet = SmartCardApplet(pin="1234")

    # PIN check
    print("\n=== Vérification du PIN ===")
    pin = input("Entrez votre code PIN : ").encode('utf-8')
    response, sw1, sw2 = send_apdu(pin, "verify_pin", applet)  # # APDU to check PIN
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
