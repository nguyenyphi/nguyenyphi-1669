from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature, encode_dss_signature
import os

class ECCCipher:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_keys(self):
        self.private_key = ec.generate_private_key(ec.SECP256R1())
        self.public_key = self.private_key.public_key()
        self.save_keys()

    def save_keys(self):
        if not os.path.exists('keys'):
            os.makedirs('keys')
        
        with open("keys/ecc_private_key.pem", "wb") as f:
            f.write(self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        with open("keys/ecc_public_key.pem", "wb") as f:
            f.write(self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    def load_keys(self):
        with open("keys/ecc_private_key.pem", "rb") as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(),
                password=None
            )
        
        with open("keys/ecc_public_key.pem", "rb") as f:
            self.public_key = serialization.load_pem_public_key(
                f.read()
            )
        return self.private_key, self.public_key

    def sign(self, message, private_key):
        signature = private_key.sign(
            message.encode(),
            ec.ECDSA(hashes.SHA256())
        )
        return signature

    def verify(self, message, signature, public_key):
        try:
            public_key.verify(
                signature,
                message.encode(),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except Exception:
            return False