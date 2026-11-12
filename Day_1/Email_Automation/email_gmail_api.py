
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .config import GOOGLE_CREDENTIALS, GOOGLE_TOKEN
from .email_creation import create_email


SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
]


def get_gmail_service():
    credentials = None

    if GOOGLE_TOKEN.exists():
        credentials = Credentials.from_authorized_user_file(
            str(GOOGLE_TOKEN),
            SCOPES,
        )

    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    if not credentials or not credentials.valid:
        if not GOOGLE_CREDENTIALS.exists():
            raise FileNotFoundError(
                "Place credentials.json inside Email_Automation."
            )

        flow = InstalledAppFlow.from_client_secrets_file(
            str(GOOGLE_CREDENTIALS),
            SCOPES,
        )

        credentials = flow.run_local_server(port=0)

    GOOGLE_TOKEN.write_text(
        credentials.to_json(),
        encoding="utf-8",
    )

    return build("gmail", "v1", credentials=credentials)


def send_gmail_email(recipient, subject, body):
    service = get_gmail_service()

    message = create_email(
        "me",
        recipient,
        subject,
        body,
    )

    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    result = service.users().messages().send(
        userId="me",
        body={"raw": encoded_message},
    ).execute()

    print("Gmail message sent.")
    print("Message ID:", result.get("id"))


def read_gmail_inbox(limit=10):
    service = get_gmail_service()

    response = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        maxResults=limit,
    ).execute()

    messages = response.get("messages", [])

    for item in messages:
        details = service.users().messages().get(
            userId="me",
            id=item["id"],
            format="metadata",
            metadataHeaders=["From", "Subject", "Date"],
        ).execute()

        print("\nMessage ID:", item["id"])

        for header in details.get("payload", {}).get("headers", []):
            print(header["name"], ":", header["value"])

    print("\nTotal messages:", len(messages))
    return messages


if __name__ == "__main__":
    read_gmail_inbox()
