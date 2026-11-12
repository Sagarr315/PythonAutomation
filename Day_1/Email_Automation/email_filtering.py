
from .email_reading import fetch_messages


def filter_by_sender(messages, sender):
    return [
        message for message in messages
        if sender.lower() in message["from"].lower()
    ]


def filter_by_subject(messages, subject):
    return [
        message for message in messages
        if subject.lower() in message["subject"].lower()
    ]


def get_unread_emails(limit=50):
    messages = fetch_messages(
        limit,
        search_criteria="UNSEEN",
    )

    print("Unread emails:", len(messages))

    for message in messages:
        print(message["from"], "|", message["subject"])

    return messages


if __name__ == "__main__":
    get_unread_emails()
