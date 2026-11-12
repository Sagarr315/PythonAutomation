
import msal
import requests

from .config import (
    MICROSOFT_CLIENT_ID,
    MICROSOFT_TENANT_ID,
)


GRAPH_URL = "https://graph.microsoft.com/v1.0"


def get_outlook_token():
    if not MICROSOFT_CLIENT_ID:
        raise ValueError(
            "Set MICROSOFT_CLIENT_ID in .env first."
        )

    app = msal.PublicClientApplication(
        MICROSOFT_CLIENT_ID,
        authority=(
            "https://login.microsoftonline.com/"
            + MICROSOFT_TENANT_ID
        ),
    )

    scopes = [
        "User.Read",
        "Mail.Read",
        "Mail.Send",
    ]

    flow = app.initiate_device_flow(scopes=scopes)

    if "user_code" not in flow:
        raise RuntimeError("Could not start Microsoft login.")

    print(flow["message"])

    result = app.acquire_token_by_device_flow(flow)

    if "access_token" not in result:
        raise RuntimeError(result.get("error_description", "Login failed"))

    return result["access_token"]


def send_outlook_email(recipient, subject, body):
    token = get_outlook_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body,
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": recipient,
                    }
                }
            ],
        },
        "saveToSentItems": True,
    }

    response = requests.post(
        f"{GRAPH_URL}/me/sendMail",
        headers=headers,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    print("Outlook email sending request accepted.")


def read_outlook_inbox(limit=10):
    token = get_outlook_token()

    headers = {
        "Authorization": f"Bearer {token}",
    }

    response = requests.get(
        f"{GRAPH_URL}/me/messages",
        headers=headers,
        params={
            "$top": limit,
            "$select": "subject,from,receivedDateTime,bodyPreview",
            "$orderby": "receivedDateTime DESC",
        },
        timeout=30,
    )

    response.raise_for_status()

    messages = response.json().get("value", [])

    for message in messages:
        sender = message.get("from", {}).get(
            "emailAddress", {}
        ).get("address", "")

        print("\nFrom:", sender)
        print("Subject:", message.get("subject"))
        print("Received:", message.get("receivedDateTime"))
        print("Preview:", message.get("bodyPreview"))

    return messages


if __name__ == "__main__":
    read_outlook_inbox()
