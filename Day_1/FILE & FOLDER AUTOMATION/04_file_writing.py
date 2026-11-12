from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "Output"


# 1. Write content into a file
def write_file(file_path, content):

    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_path.write_text(content, encoding="utf-8")

    print("Content written:", file_path.name)


# 2. Append content to an existing file
def append_to_file(file_path, content):

    file_path = Path(file_path)

    if not file_path.exists():
        print("File does not exist:", file_path.name)
        return

    with open(file_path, "a", encoding="utf-8") as file:
        file.write(content)

    print("Content appended:", file_path.name)


# 3. Write multiple lines
def write_multiple_lines(file_path, lines):

    file_path = Path(file_path)

    with open(file_path, "w", encoding="utf-8") as file:

        for line in lines:
            file.write(line + "\n")

    print("Multiple lines written:", file_path.name)


# 4. Read and display file content
def display_file(file_path):

    file_path = Path(file_path)

    if not file_path.exists():
        print("File not found.")
        return

    print("\nFile Content:")
    print(file_path.read_text(encoding="utf-8"))


# 5. Main execution
if __name__ == "__main__":

    report_file = OUTPUT_DIR / "Writing_Report.txt"

    print("\n--- Write File ---")
    write_file(
        report_file,
        "Automation Report\n"
        "Status: Started\n"
    )

    print("\n--- Append Content ---")
    append_to_file(
        report_file,
        "Status: Completed\n"
    )

    print("\n--- Write Multiple Lines ---")
    write_multiple_lines(
        OUTPUT_DIR / "Employee_Details.txt",
        [
            "Employee_001",
            "Employee_002",
            "Employee_003"
        ]
    )

    print("\n--- Display File ---")
    display_file(report_file)

    print("\nWriting operations completed!")
