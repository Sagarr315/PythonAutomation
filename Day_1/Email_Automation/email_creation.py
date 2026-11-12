
from email.message import EmailMessage
from pathlib import Path
import mimetypes


def create_email(
    sender,
    recipient,
    subject,
    body,
    html_body=None,
    attachment_paths=None,
):
    message = EmailMessage()

    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject

    message.set_content(body)

    if html_body:
        message.add_alternative(
            html_body,
            subtype="html",
        )

    for attachment_path in attachment_paths or []:
        path = Path(attachment_path)

        if not path.is_file():
            raise FileNotFoundError(path)

        content_type, encoding = mimetypes.guess_type(path.name)

        if content_type is None or encoding is not None:
            content_type = "application/octet-stream"

        maintype, subtype = content_type.split("/", 1)

        with open(path, "rb") as file:
            message.add_attachment(
                file.read(),
                maintype=maintype,
                subtype=subtype,
                filename=path.name,
            )

    return message


if __name__ == "__main__":
    message = create_email(
        "sender@example.com",
        "recipient@example.com",
        "Python Automation Test",
        "This is a sample email created using Python.",
        "<h2>Python Automation</h2><p>Sample HTML email.</p>",
    )

    print(message)
