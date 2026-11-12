from pathlib import Path


# Project folder location
BASE_DIR = Path(__file__).resolve().parent

# Output folder location
OUTPUT_DIR = BASE_DIR / "Output"


# 1. Read complete file
def read_complete_file(file_path):

    file_path = Path(file_path)

    if not file_path.exists():
        print("File not found:", file_path.name)
        return

    content = file_path.read_text(encoding="utf-8")

    print("\n--- Complete File Content ---")
    print(content)


# 2. Read file line by line
def read_line_by_line(file_path):

    file_path = Path(file_path)

    if not file_path.exists():
        print("File not found:", file_path.name)
        return

    print("\n--- Reading Line By Line ---")

    with open(file_path, "r", encoding="utf-8") as file:

        for line_number, line in enumerate(file, start=1):

            print(f"Line {line_number}: {line.rstrip()}")


# 3. Read multiple files
def read_multiple_files(folder_path):

    folder_path = Path(folder_path)

    print("\n--- Reading Multiple Files ---")

    files = list(folder_path.glob("*.txt"))

    if not files:
        print("No text files found.")
        return

    for file_path in files:

        print(f"\nFile Name: {file_path.name}")

        content = file_path.read_text(encoding="utf-8")

        print(content)


# 4. Search specific text in files
def search_text_in_files(folder_path, search_text):

    folder_path = Path(folder_path)

    print("\n--- Searching Text ---")

    files = folder_path.glob("*.txt")

    for file_path in files:

        content = file_path.read_text(encoding="utf-8")

        if search_text.lower() in content.lower():

            print("Text found in:", file_path.name)


# 5. Count lines, words and characters
def get_file_statistics(file_path):

    file_path = Path(file_path)

    if not file_path.exists():
        print("File not found:", file_path.name)
        return

    content = file_path.read_text(encoding="utf-8")

    lines = len(content.splitlines())
    words = len(content.split())
    characters = len(content)

    print("\n--- File Statistics ---")
    print("File:", file_path.name)
    print("Lines:", lines)
    print("Words:", words)
    print("Characters:", characters)


# 6. Main execution
if __name__ == "__main__":

    report_file = OUTPUT_DIR / "Report.txt"

    print("\n1. Read Complete File")
    read_complete_file(report_file)

    print("\n2. Read Line By Line")
    read_line_by_line(report_file)

    print("\n3. Read Multiple Files")
    read_multiple_files(OUTPUT_DIR)

    print("\n4. Search Text")
    search_text_in_files(
        OUTPUT_DIR,
        "sample"
    )

    print("\n5. File Statistics")
    get_file_statistics(report_file)

    print("\nFile reading operations completed!")
