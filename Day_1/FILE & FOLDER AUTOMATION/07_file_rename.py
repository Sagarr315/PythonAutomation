from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "Output"


# 1. Rename a single file
def rename_file(file_path, new_name):

    file_path = Path(file_path)

    if not file_path.is_file():
        print("File not found.")
        return

    new_path = file_path.with_name(new_name)

    if new_path.exists():
        print("New filename already exists.")
        return

    file_path.rename(new_path)

    print("Renamed:", file_path.name, "->", new_path.name)


# 2. Rename multiple files with a prefix
def rename_multiple_files(folder_path, prefix):

    folder_path = Path(folder_path)

    if not folder_path.is_dir():
        print("Folder not found.")
        return

    files = sorted(
        file for file in folder_path.iterdir()
        if file.is_file()
    )

    for number, file_path in enumerate(files, start=1):

        new_name = f"{prefix}_{number:03}{file_path.suffix}"
        new_path = file_path.with_name(new_name)

        if new_path.exists():
            print("Skipped:", new_name)
            continue

        file_path.rename(new_path)

        print("Renamed:", file_path.name, "->", new_name)


# 3. Change file extension
def change_file_extension(file_path, new_extension):

    file_path = Path(file_path)

    if not file_path.is_file():
        print("File not found.")
        return

    if not new_extension.startswith("."):
        new_extension = "." + new_extension

    new_path = file_path.with_suffix(new_extension)

    if new_path.exists():
        print("Destination filename already exists.")
        return

    file_path.rename(new_path)

    print("Extension changed:", new_path.name)


# 4. Main execution
if __name__ == "__main__":

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    sample_file = OUTPUT_DIR / "Old_Report.txt"

    if not sample_file.exists():
        sample_file.write_text(
            "Sample report content.",
            encoding="utf-8"
        )

    print("\n--- Rename Single File ---")
    rename_file(sample_file, "New_Report.txt")

    print("\nFile rename operations completed!")
