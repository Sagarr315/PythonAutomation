from docx import Document

from .config import SAMPLE_WORD


def read_word_document(file_path):
    document = Document(file_path)

    print("\n--- Paragraphs ---")

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            print(paragraph.text)

    print("\n--- Tables ---")

    for table_number, table in enumerate(document.tables, start=1):
        print("Table:", table_number)

        for row in table.rows:
            print([cell.text for cell in row.cells])


if __name__ == "__main__":
    read_word_document(SAMPLE_WORD)