
import smtplib
import ssl

from .config import (
    EMAIL_ADDRESS,
    EMAIL_APP_PASSWORD,
    SMTP_SERVER,
    SMTP_PORT,
    validate_email_credentials,
)


def send_email(message):
    validate_email_credentials()

    context = ssl.create_default_context()

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()

        server.login(
            EMAIL_ADDRESS,
            EMAIL_APP_PASSWORD,
        )

        server.send_message(message)

    print("REAL EMAIL SENT SUCCESSFULLY!")


if __name__ == "__main__":
    from .email_creation import create_email

    message = create_email(
        EMAIL_ADDRESS,
        EMAIL_ADDRESS,
        "Python Email Test",
        "This is a real test email sent using Python SMTP.",
    )

    send_email(message)
