from pathlib import Path

# Docker volume mount points
DATA_DIR = Path("/data")
CRON_DIR = Path("/cron")

# Persistent seed storage
SEED_FILE = DATA_DIR / "seed.txt"
