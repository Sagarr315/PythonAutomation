from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = BASE_DIR / "Input"
OUTPUT_DIR = BASE_DIR / "Output"
ARCHIVE_DIR = BASE_DIR / "Archive"

for folder in (INPUT_DIR, OUTPUT_DIR, ARCHIVE_DIR):
    folder.mkdir(parents=True, exist_ok=True)

NOTEPAD_FILE = OUTPUT_DIR / "Python_Automation_Demo.txt"
SCREENSHOT_FILE = OUTPUT_DIR / "Desktop_Screenshot.png"