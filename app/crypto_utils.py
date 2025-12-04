from pathlib import Path
import base64

from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import hashes, serialization


def generate_rsa_keypair(key_size: int = 4096):
    """
    Generate RSA 4096-bit key pair with public exponent 65537
    
    Returns:
        Tuple of (private_key, public_key) objects
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )
    public_key = private_key.public_key()
    return private_key, public_key


def load_private_key(path: str = "student_private.pem"):
    """Load RSA private key from PEM file"""
    data = Path(path).read_bytes()
    return serialization.load_pem_private_key(data, password=None)


def load_public_key(path: str):
    """Load RSA public key from PEM file"""
    data = Path(path).read_bytes()
    return serialization.load_pem_public_key(data)


def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    """
    Decrypt base64-encoded encrypted seed using RSA/OAEP with SHA-256
    
    Args:
        encrypted_seed_b64: Base64-encoded ciphertext
        private_key: RSA private key object
    
    Returns:
        Decrypted hex seed (64-character string)
    """
    # Base64 decode
    ciphertext = base64.b64decode(encrypted_seed_b64)
    
    # RSA/OAEP decrypt with SHA-256, MGF1(SHA-256)
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    
    # Decode to UTF-8 string
    hex_seed = plaintext.decode("utf-8").strip()
    
    # Validate: must be 64-character hex string
    if len(hex_seed) != 64:
        raise ValueError("Seed must be 64 hex characters")
    if any(c not in "0123456789abcdef" for c in hex_seed.lower()):
        raise ValueError("Seed must be lowercase hex")
    
    return hex_seed.lower()


def sign_message(message: str, private_key) -> bytes:
    """
    Sign a message using RSA-PSS with SHA-256
    
    Args:
        message: Message to sign (commit hash)
        private_key: RSA private key object
    
    Returns:
        Signature bytes
    """
    # Encode message as ASCII/UTF-8 bytes
    message_bytes = message.encode("utf-8")
    
    # Sign using RSA-PSS with SHA-256, max salt length
    signature = private_key.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    
    return signature


def encrypt_with_public_key(data: bytes, public_key) -> bytes:
    """
    Encrypt data using RSA/OAEP with public key
    
    Args:
        data: Data to encrypt (signature bytes)
        public_key: RSA public key object
    
    Returns:
        Encrypted ciphertext bytes
    """
    ciphertext = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    
    return ciphertext

