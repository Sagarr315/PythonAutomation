
from .email_reading import fetch_messages


def search_emails(sender=None, subject=None, limit=50):
    messages = fetch_messages(limit)

    matched_messages = []

    for message in messages:
        sender_match = (
            sender is None
            or sender.lower() in message["from"].lower()
        )

        subject_match = (
            subject is None
            or subject.lower() in message["subject"].lower()
        )

        if sender_match and subject_match:
            matched_messages.append(message)

    print("\nMatching emails:", len(matched_messages))

    for message in matched_messages:
        print("From:", message["from"])
        print("Subject:", message["subject"])
        print("Date:", message["date"])
        print("-------------------------")

    return matched_messages


if __name__ == "__main__":
    search_emails(subject="Invoice")
