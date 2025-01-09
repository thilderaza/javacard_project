from smartcard.System import readers
from datetime import datetime
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from smartcard.System import readers
from applet import SmartCardApplet  
import requests

# Different articles available
def display_articles():
    articles = {
        1:{"name": "Water bottle","price": 1.10},
        2:{"name": "Haribo Dragibus", "price": 1.40}
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
            choice = int(input("Enter the number of the article to add (0 to end) : "))
            if choice == 0:
                break
            if choice in articles:
                item = articles[choice]
                total += item["price"]
                print(f"Added : {item['name']} (${item['prix']:.2f})")
            else:
                print("Invalid option, please try again.")
        except ValueError:
            print("Invalid entry, please enter a number.")
    
    return total

def send_apdu(data,applet):
    # Retrieves the list of available drives
    r = readers()
    if len(r) > 0:
        print("Readers available: ",r)
    else:
        print("There is no reader.")

    reader = r[0]
    connection = reader.createConnection()
    connection.connect()
    print("You are connected to the reader: ",reader)


    #Command APDU (transmission of data)
    APDU = [0x80, 0x10, 0x00, 0x00, len(data)] + data
    try:
        response,sw1,sw2 = connection.transmit(APDU)

        # sw values returned by the card
        # Success
        if sw1 == 0x90 and sw2 == 0x00:
            print("Transaction completed.")

        # Error (Due to an access problem (incorrect/unverified PIN, data or file length problem) )
        else:
            print(f"Error : SW1={sw1}, SW2={sw2}")
        response, sw1, sw2 = applet.process_apdu(APDU)
        return response, sw1, sw2
    except Exception as e:
            print("Error when the transmission APDU :", str(e))
            return None, None, None

# Récupérer l'horodatage signé
def get_signed_timestamp():
    response = requests.get("http://localhost:5000/get_timestamp")
    if response.status_code == 200:
        data = response.json()
        print("Signed timestamp recovered :", data)
        return data
    else:
        print("Error when the timestamp recovery :", response.json())
        return None
    
# Send the signed transaction to server
def send_to_server(transaction, signature, card_public_key):

    response = requests.post("http://localhost:5000/verify_transaction", json={
        "transaction": transaction,
        "signature": signature.hex(),
        "card_public_key": card_public_key.decode('utf-8')
    })
    print("Response of serveur :", response.json())
