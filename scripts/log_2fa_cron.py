#!/usr/bin/env python3
"""
Cron script to log 2FA codes every minute
"""
import sys
from datetime import datetime, timezone

from app.totp_utils import generate_totp_code
from app.config import SEED_FILE


def main():
    """Generate and log TOTP code with UTC timestamp"""
    try:
        # Check if seed file exists
        if not SEED_FILE.exists():
            print("Seed file not found", file=sys.stderr)
            return
        
        # Read hex seed
        hex_seed = SEED_FILE.read_text(encoding="utf-8").strip()
        
        # Generate TOTP code
        code = generate_totp_code(hex_seed)
        
        # Get current UTC timestamp
        now_utc = datetime.now(timezone.utc)
        timestamp = now_utc.strftime("%Y-%m-%d %H:%M:%S")
        
        # Output formatted line (appended by cron)
        print(f"{timestamp} - 2FA Code: {code}")
        
    except Exception as e:
        print(f"Error in cron script: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
