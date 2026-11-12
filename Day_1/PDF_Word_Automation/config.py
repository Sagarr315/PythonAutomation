from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = BASE_DIR / "Input"
OUTPUT_DIR = BASE_DIR / "Output"
ARCHIVE_DIR = BASE_DIR / "Archive"

for folder in (INPUT_DIR, OUTPUT_DIR, ARCHIVE_DIR):
    folder.mkdir(parents=True, exist_ok=True)

SAMPLE_PDF = INPUT_DIR / "Sample_Report.pdf"
SAMPLE_FORM = INPUT_DIR / "Sample_Form.pdf"
SAMPLE_WORD = INPUT_DIR / "Sample_Document.docx"