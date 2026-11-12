
from pathlib import Path

from .config import OUTPUT_DIR
from .email_reading import fetch_messages
from .email_creation import create_email


def create_email_with_attachment(
    sender,
    recipient,
    subject,
    body,
    attachment_path,
):
    return create_email(
        sender,
        recipient,
        subject,
        body,
        attachment_paths=[attachment_path],
    )


def download_attachments(messages):
    output_folder = OUTPUT_DIR / "Downloaded_Attachments"
    output_folder.mkdir(parents=True, exist_ok=True)

    downloaded = 0

    for item in messages:
        message = item["message"]

        for part in message.walk():
            filename = part.get_filename()

            if not filename:
                continue

            payload = part.get_payload(decode=True)

            if not payload:
                continue

            safe_name = Path(filename).name
            output_file = output_folder / safe_name

            if output_file.exists():
                output_file = output_folder / (
                    f"{downloaded + 1}_{safe_name}"
                )

            with open(output_file, "wb") as file:
                file.write(payload)

            downloaded += 1
            print("Downloaded:", output_file.name)

    print("Total attachments downloaded:", downloaded)


if __name__ == "__main__":
    messages = fetch_messages(limit=20)
    download_attachments(messages)
