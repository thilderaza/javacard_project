from smartcard.System import readers

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

def send_apdu(data):
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
        return response, sw1,sw2
    except Exception as e:
            print("Erreur lors de la transmission APDU :", str(e))
            return None, None, None


if __name__ == "__main__":

    # Afficher les artices
    article = display_articles()

    # Permettre la sélection des articles
    selected_items, total = select_art(article)

    # Afficher le résultat
    print(f"\nTotal de la transaction : ${total:.2f} ")

    # Données à transmettre via APDU
    response, sw1, sw2 = send_apdu(total)
    
