from flask import Flask, request, jsonify
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from datetime import datetime

app = Flask(__name__)

# paire de clés RSA pour le serveur
server_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
server_public_key = server_private_key.public_key()

@app.route("/verify_transaction", methods=["POST"])
def verify_transaction():
    data = request.json
    transaction = data["transaction"].encode('utf-8')
    signature = bytes.fromhex(data["signature"])
    card_public_key_pem = data["card_public_key"]

    # Charger la clé publique de la carte
    from cryptography.hazmat.primitives import serialization
    card_public_key = serialization.load_pem_public_key(card_public_key_pem.encode('utf-8'))

    # Valider la signature
    try:
        card_public_key.verify(
            signature,
            transaction,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        transactions.append({"transaction": transaction.decode('utf-8'), "verified": True})
        return jsonify({"status": "success", "message": "Transaction vérifiée avec succès"}), 200
    except Exception as e:
        return jsonify({"status": "failure", "message": f"Signature invalide : {str(e)}"}), 400

@app.route("/get_timestamp", methods=["GET"])
def get_timestamp():
    timestamp = datetime.utcnow().isoformat()
    signature = server_private_key.sign(
        timestamp.encode('utf-8'),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return jsonify({
        "timestamp": timestamp,
        "signature": signature.hex()
    })

@app.route("/is_card_stolen", methods=["GET"])
def is_card_stolen():
    """
    Endpoint pour vérifier si une carte est volée.
    Paramètre : card_id=<ID de la carte>
    """
    card_id = request.args.get("card_id")
    if card_id in stolen_cards:
        return jsonify({"status": "stolen", "message": f"Carte {card_id} est volée"}), 200
    return jsonify({"status": "ok", "message": f"Carte {card_id} n'est pas volée"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)