
import imaplib
import email

from email.header import decode_header

from .config import (
    EMAIL_ADDRESS,
    EMAIL_APP_PASSWORD,
    IMAP_SERVER,
    IMAP_PORT,
    validate_email_credentials,
)


def decode_email_header(value):
    if not value:
        return ""

    parts = decode_header(value)
    result = []

    for content, encoding in parts:
        if isinstance(content, bytes):
            result.append(
                content.decode(encoding or "utf-8", errors="replace")
            )
        else:
            result.append(content)

    return "".join(result)


def extract_email_body(message):
    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            disposition = part.get_content_disposition()

            if content_type == "text/plain" and disposition != "attachment":
                payload = part.get_payload(decode=True)

                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    return payload.decode(charset, errors="replace")

    else:
        payload = message.get_payload(decode=True)

        if payload:
            charset = message.get_content_charset() or "utf-8"
            return payload.decode(charset, errors="replace")

    return ""


def fetch_messages(limit=10, search_criteria="ALL"):
    validate_email_credentials()

    mailbox = imaplib.IMAP4_SSL(
        IMAP_SERVER,
        IMAP_PORT,
    )

    try:
        mailbox.login(
            EMAIL_ADDRESS,
            EMAIL_APP_PASSWORD,
        )

        mailbox.select("INBOX", readonly=True)

        status, data = mailbox.search(
            None,
            search_criteria,
        )

        if status != "OK":
            raise RuntimeError("Could not search inbox.")

        message_ids = data[0].split()
        selected_ids = message_ids[-limit:]

        results = []

        for message_id in reversed(selected_ids):
            status, response = mailbox.fetch(
                message_id,
                "(RFC822)",
            )

            if status != "OK":
                continue

            raw_message = response[0][1]
            message = email.message_from_bytes(raw_message)

            results.append({
                "id": message_id.decode(),
                "from": decode_email_header(message.get("From")),
                "subject": decode_email_header(message.get("Subject")),
                "date": message.get("Date", ""),
                "body": extract_email_body(message),
                "message": message,
            })

        return results

    finally:
        try:
            mailbox.logout()
        except Exception:
            pass


def read_inbox(limit=10):
    messages = fetch_messages(limit)

    for item in messages:
        print("\n------------------------------")
        print("From:", item["from"])
        print("Subject:", item["subject"])
        print("Date:", item["date"])
        print("Body:", item["body"][:500])

    print("\nTotal emails read:", len(messages))
    return messages


if __name__ == "__main__":
    read_inbox()
