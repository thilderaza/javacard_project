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
    def sign_and_encrypt_data(self, data):
        if not isinstance(data, bytes):
            raise ValueError("Data must be in bytes format.")

        signature = self.private_key.sign(
            data,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
    
        # Encrypt signed data with the server public key
        encrypted_data = self.server_public_key.encrypt(
            signature,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_data

    # Returns the public key in PEM format
    def get_public_key(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
    
    # Manages the reconstitution of data sent via multiple APDUs
    def handle_multi_apdu(self, apdu_chunks):
        full_data = b''  # Initialize an empty byte string to accumulate the data
        for chunk in apdu_chunks:
            if not isinstance(chunk, bytes):
                raise ValueError("Each APDU chunk must be in bytes format.")
            full_data += chunk  # Concatenate each chunk to the full data

        return full_data

    # Divides data into fixed-size fragments
    def split_into_apdu_chunks(self, data, chunk_size=256):
        if not isinstance(data, bytes):
            raise ValueError("Data must be in bytes format.")
        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        return chunks

    # Send the IP address
    def get_server_ip(self, sign=False):
        server_ip = b"192.168.1.1"  # Example
        if sign:
            signed_ip = self.private_key.sign(
                server_ip,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return signed_ip
        return server_ip