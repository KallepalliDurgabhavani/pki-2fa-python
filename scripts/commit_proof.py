#!/usr/bin/env python3
"""
Generate commit proof: sign commit hash and encrypt signature
"""
import base64

from app.crypto_utils import (
    load_private_key,
    load_public_key,
    sign_message,
    encrypt_with_public_key,
)


def main():
    """Generate encrypted commit signature"""
    # Get commit hash
    commit_hash = input("Enter commit hash (40-char hex): ").strip()
    
    if len(commit_hash) != 40:
        raise ValueError("Commit hash must be 40 characters")
    
    print(f"📝 Commit hash: {commit_hash}")
    
    # Load keys
    print("🔑 Loading keys...")
    private_key = load_private_key("student_private.pem")
    instructor_pub = load_public_key("instructor_public.pem")
    
    # Sign commit hash with student private key
    print("✍️  Signing commit hash with RSA-PSS-SHA256...")
    signature = sign_message(commit_hash, private_key)
    
    # Encrypt signature with instructor public key
    print("🔒 Encrypting signature with instructor public key...")
    encrypted_sig = encrypt_with_public_key(signature, instructor_pub)
    
    # Base64 encode
    b64 = base64.b64encode(encrypted_sig).decode("utf-8")
    
    print("\n" + "="*60)
    print("✅ Encrypted commit signature (single line):")
    print("="*60)
    print(b64)
    print("="*60)
    print("\n⚠️  Copy the ENTIRE base64 string above (single line, no breaks)")


if __name__ == "__main__":
    main()
