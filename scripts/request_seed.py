#!/usr/bin/env python3
"""
Request encrypted seed from instructor API
"""
import requests
from pathlib import Path


API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/"


STUDENT_ID = "22MH1A05H9"
GITHUB_REPO_URL = "https://github.com/KallepalliDurgabhavani/pki-2fa-python"


def load_public_key_text(path: str) -> str:
    """Load public key as text"""
    pem = Path(path).read_text(encoding="utf-8")
    return pem


def request_seed():
    """Request encrypted seed from instructor API"""
    # Load student public key
    public_key_pem = load_public_key_text("student_public.pem")
    
    # Prepare payload
    payload = {
        "student_id": STUDENT_ID,
        "github_repo_url": GITHUB_REPO_URL,
        "public_key": public_key_pem,
    }
    
    print(f"🔄 Requesting encrypted seed from instructor API...")
    print(f"   Student ID: {STUDENT_ID}")
    print(f"   GitHub Repo: {GITHUB_REPO_URL}")
    
    # Send POST request
    try:
        resp = requests.post(API_URL, json=payload, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        print(f"❌ API request failed: {e}")
        raise
    
    # Parse response
    data = resp.json()
    print(f"📥 Response: {data.get('status')}")
    
    if data.get("status") != "success":
        raise RuntimeError(f"API error: {data}")
    
    # Save encrypted seed
    encrypted_seed = data["encrypted_seed"].strip()
    Path("encrypted_seed.txt").write_text(encrypted_seed, encoding="utf-8")
    
    print("✅ Encrypted seed saved to encrypted_seed.txt")


if __name__ == "__main__":
    request_seed()
