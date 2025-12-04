#!/usr/bin/env python3
"""
Generate RSA 4096-bit key pair for student identity
"""
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generate_rsa_keypair():
    """Generate and save RSA 4096-bit key pair"""
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )
    
    # Derive public key
    public_key = private_key.public_key()
    
    # Save private key
    with open("student_private.pem", "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )
    
    # Save public key
    with open("student_public.pem", "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )
    
    print("✅ Keys generated successfully:")
    print("   - student_private.pem")
    print("   - student_public.pem")


if __name__ == "__main__":
    generate_rsa_keypair()
