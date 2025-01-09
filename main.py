from applet import SmartCardApplet
from terminal_app import send_apdu, display_articles, select_art, get_signed_timestamp, send_to_server

if __name__ == "__main__":
    # instance of the simulated applet
    applet = SmartCardApplet(pin="1234")

    # Verify PIN
    print("\n=== Verification of PIN ===")
    pin = input("Enter your PIN code : ").encode('utf-8')  # Ask user for the PIN 
    response, sw1, sw2 = send_apdu(pin, "verify_pin", applet)  # APDU for verify the PIN
    if sw1 == 0x90:
        print("PIN successfully verified.")
    else:
        print("PIN verification failed.")
        exit()  # Stop the program while the PIN verification failed

    # Display and select articles
    print("\n=== selection of articles ===")
    articles = display_articles()  # Dispaly available articles
    total = select_art(articles)  # Allow selection and calculates the total amount 

    # Display the amount of the transaction
    print(f"\nAmount of the transaction : ${total:.2f}")

    #  Retrieve signed timestamp from le server
    print("\n=== Retrieve signed timestamp ===")
    timestamp_data = get_signed_timestamp()  # Call the server for retrieve signed timestamp
    if not timestamp_data:
        print("Error : Unable to retrieve signed timestamp.")
        exit()

    # Prepare transaction data
    transaction_data = f"total={int(total * 100)}&timestamp={timestamp_data['timestamp']}"
    print(f"Prepared transaction : {transaction_data}")

    # Card signature of transaction data
    print("\n=== Signature of the transaction for the card ===")
    apdu_sign_data = [0x80, 0x10, 0x00, 0x00, len(transaction_data)] + list(transaction_data.encode('utf-8'))
    response, sw1, sw2 = applet.process_apdu(apdu_sign_data)  # Call Applet to signe
    if sw1 == 0x90:
        print("Transaction successfully signed.")
    else:
        print("Transaction signature failed.")
        exit()

    # Send signed transaction to server for verification
    print("\n=== Sending the signed transaction to the server ===")
    card_public_key = applet.get_public_key()  # Recovers the card's public key
    send_to_server(transaction_data, response, card_public_key)  # Send to server

    print("\n=== End of transaction ===")
