
from .email_creation import create_email
from .config import OUTPUT_DIR, EMAIL_ADDRESS


def simulate_email(recipient, subject, body):
    sender = EMAIL_ADDRESS or "simulation@example.com"

    message = create_email(
        sender,
        recipient,
        subject,
        body,
    )

    output_file = OUTPUT_DIR / "Simulated_Email.eml"

    with open(output_file, "wb") as file:
        file.write(bytes(message))

    print("SIMULATION COMPLETED")
    print("No email was sent.")
    print("Email saved:", output_file)

    return output_file


if __name__ == "__main__":
    simulate_email(
        "recipient@example.com",
        "Test Email",
        "This email is only a simulation.",
    )
