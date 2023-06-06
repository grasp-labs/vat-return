"""
Script to create a jwk object used for defining the public key in ID
porten integration.
"""
import hashlib
import secrets
import base64


from cryptography.hazmat.primitives.asymmetric import rsa

if __name__ == "__main__":

    # Generate a new RSA private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,  # Commonly used value for the public exponent (e)
        key_size=2048,  # Use 2048 bits in accordance with documentation.
    )

    # Access the modulus (n)
    modulus = private_key.public_key().public_numbers().n

    print(modulus)

    # Sequence to add into each log in operation. Remember these values
    # in notepad for now.
    code_verifier = secrets.token_urlsafe(64)
    print(code_verifier)

    code_challenge = base64.urlsafe_b64decode(
        hashlib.sha256(
            code_verifier.encode()
        ).digest()
    ).rstrip(b="=").decode()

    print(code_challenge)
