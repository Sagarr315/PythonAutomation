
from .config import EMAIL_ADDRESS, OUTPUT_DIR

from .email_creation import create_email
from .email_simulation import simulate_email
from .email_sending import send_email
from .email_reading import read_inbox, fetch_messages
from .email_search import search_emails
from .email_filtering import get_unread_emails
from .email_attachments import download_attachments

from .email_gmail_api import (
    send_gmail_email,
    read_gmail_inbox,
)

from .email_outlook import (
    send_outlook_email,
    read_outlook_inbox,
)


def display_menu():
    print("\n======================================")
    print("       PYTHON EMAIL AUTOMATION")
    print("======================================")
    print("1. Simulate Email (No Real Sending)")
    print("2. Create Email Message")
    print("3. Send Real Email using SMTP")
    print("4. Read Inbox using IMAP")
    print("5. Search Emails")
    print("6. Read Unread Emails")
    print("7. Download Email Attachments")
    print("8. Send Email with Attachment")
    print("9. Send Email using Gmail API")
    print("10. Read Gmail using Gmail API")
    print("11. Send Email using Outlook API")
    print("12. Read Outlook Inbox")
    print("0. Exit")
    print("====================================")


def confirm_real_send():
    confirmation = input(
        "\nThis sends a REAL email. Type SEND to continue: "
    ).strip()

    return confirmation == "SEND"


def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                recipient = input("Recipient email: ")
                subject = input("Subject: ")
                body = input("Email body: ")

                simulate_email(recipient, subject, body)

            elif choice == "2":
                recipient = input("Recipient email: ")
                subject = input("Subject: ")
                body = input("Email body: ")

                message = create_email(
                    EMAIL_ADDRESS or "simulation@example.com",
                    recipient,
                    subject,
                    body,
                )

                output_file = OUTPUT_DIR / "Created_Email.eml"

                with open(output_file, "wb") as file:
                    file.write(message.as_bytes())

                print("Email created:", output_file)

            elif choice == "3":
                recipient = input("Recipient email: ")
                subject = input("Subject: ")
                body = input("Email body: ")

                if confirm_real_send():
                    message = create_email(
                        EMAIL_ADDRESS,
                        recipient,
                        subject,
                        body,
                    )
                    send_email(message)
                else:
                    print("Email sending cancelled.")

            elif choice == "4":
                read_inbox(limit=10)

            elif choice == "5":
                sender = input(
                    "Sender email (leave blank to skip): "
                ).strip()

                subject = input(
                    "Subject keyword (leave blank to skip): "
                ).strip()

                search_emails(
                    sender=sender or None,
                    subject=subject or None,
                )

            elif choice == "6":
                get_unread_emails()

            elif choice == "7":
                messages = fetch_messages(limit=20)
                download_attachments(messages)

            elif choice == "8":
                recipient = input("Recipient email: ")
                subject = input("Subject: ")
                body = input("Email body: ")
                attachment = input("Attachment file path: ")

                if confirm_real_send():
                    message = create_email(
                        EMAIL_ADDRESS,
                        recipient,
                        subject,
                        body,
                        attachment_paths=[attachment],
                    )
                    send_email(message)
                else:
                    print("Email sending cancelled.")

            elif choice == "9":
                recipient = input("Recipient email: ")
                subject = input("Subject: ")
                body = input("Email body: ")

                if confirm_real_send():
                    send_gmail_email(recipient, subject, body)
                else:
                    print("Email sending cancelled.")

            elif choice == "10":
                read_gmail_inbox()

            elif choice == "11":
                recipient = input("Recipient email: ")
                subject = input("Subject: ")
                body = input("Email body: ")

                if confirm_real_send():
                    send_outlook_email(
                        recipient,
                        subject,
                        body,
                    )
                else:
                    print("Email sending cancelled.")

            elif choice == "12":
                read_outlook_inbox()

            elif choice == "0":
                print("Email Automation application closed.")
                break

            else:
                print("Invalid choice.")

        except Exception as error:
            print("\nOperation failed:", error)

        if choice != "0":
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
