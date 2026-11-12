
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = BASE_DIR / "Input"
OUTPUT_DIR = BASE_DIR / "Output"
ARCHIVE_DIR = BASE_DIR / "Archive"

for folder in (INPUT_DIR, OUTPUT_DIR, ARCHIVE_DIR):
    folder.mkdir(parents=True, exist_ok=True)

load_dotenv(BASE_DIR / ".env")

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD", "")

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))

GOOGLE_CREDENTIALS = BASE_DIR / "credentials.json"
GOOGLE_TOKEN = BASE_DIR / "token.json"

MICROSOFT_CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID", "")
MICROSOFT_TENANT_ID = os.getenv(
    "MICROSOFT_TENANT_ID", "common"
)


def validate_email_credentials():
    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD:
        raise ValueError(
            "Set EMAIL_ADDRESS and EMAIL_APP_PASSWORD in .env"
        )
