from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import os


class SmartCardApplet:

    # Stores PIN and generates RSA key pair
    def __init__(self, pin="1234"):
        self.pin = pin
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=512)
        self.public_key = self.private_key.public_key()
        print("Smart card initialized with a PIN and RSA key pair.")

    # Verifies if the pIN is correct
    def verify_pin(self, pin_input):
        boolean = self.pin == pin_input
        if(boolean):
            print("Pin code verified")
        else:
            print("Pin code not verified")
        return boolean

    # Signs data with private key
    def sign_data(self, data):
        
        if not isinstance(data, bytes):
            raise ValueError("Data must be in bytes format.")
        signature = self.private_key.sign(
            data,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return signature

    # Returns the public key in PEM format
    def get_public_key(self):
        # Serialize the public key to PEM format
        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem
    
    # Manages the reconstitution of data sent via multiple APDUs
    def handle_multi_apdu(self, apdu_chunks):
        full_data = b''  # Initialize an empty byte string to accumulate the data
        for chunk in apdu_chunks:
            if not isinstance(chunk, bytes):
                raise ValueError("Each APDU chunk must be in bytes format.")
            full_data += chunk  # Concatenate each chunk to the full data

        return full_data


