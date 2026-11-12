from pypdf import PdfReader

from .config import SAMPLE_PDF


def read_pdf_metadata(file_path):
    reader = PdfReader(str(file_path))

    print("Total pages:", len(reader.pages))

    metadata = reader.metadata

    if metadata:
        print("Title:", metadata.title)
        print("Author:", metadata.author)
        print("Subject:", metadata.subject)
        print("Creator:", metadata.creator)
    else:
        print("No metadata available.")


if __name__ == "__main__":
    read_pdf_metadata(SAMPLE_PDF)