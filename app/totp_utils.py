import base64
import time

import pyotp


def hex_to_base32(hex_seed: str) -> str:
    """
    Convert 64-character hex seed to base32 encoding for TOTP
    
    Args:
        hex_seed: 64-character hex string
    
    Returns:
        Base32-encoded seed string
    """
    # Convert hex to bytes
    seed_bytes = bytes.fromhex(hex_seed)
    
    # Encode to base32
    b32 = base64.b32encode(seed_bytes).decode("utf-8")
    
    return b32


def generate_totp_code(hex_seed: str) -> str:
    """
    Generate current TOTP code from hex seed
    
    Configuration:
    - Algorithm: SHA-1 (standard for TOTP)
    - Period: 30 seconds
    - Digits: 6
    
    Args:
        hex_seed: 64-character hex string
    
    Returns:
        6-digit TOTP code as string
    """
    # Convert hex to base32
    base32_seed = hex_to_base32(hex_seed)
    
    # Create TOTP object with standard settings
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)
    
    # Generate current code
    return totp.now()


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify TOTP code with time window tolerance
    
    Args:
        hex_seed: 64-character hex string
        code: 6-digit code to verify
        valid_window: Number of periods before/after to accept (default 1 = ±30s)
    
    Returns:
        True if code is valid, False otherwise
    """
    # Convert hex to base32
    base32_seed = hex_to_base32(hex_seed)
    
    # Create TOTP object
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)
    
    # Verify with time window tolerance (±30 seconds)
    return totp.verify(code, valid_window=valid_window)


def seconds_remaining_in_period(interval: int = 30) -> int:
    """
    Calculate remaining seconds in current TOTP period
    
    Args:
        interval: TOTP time period in seconds (default 30)
    
    Returns:
        Remaining seconds (0-29)
    """
    now = int(time.time())
    return interval - (now % interval)
