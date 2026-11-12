from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "Output"


# 1. Delete a single file
def delete_file(file_path):

    file_path = Path(file_path)

    if not file_path.is_file():
        print("File not found.")
        return

    confirmation = input(
        f"Are you sure you want to delete {file_path.name}? (yes/no): "
    )

    if confirmation.lower() == "yes":

        file_path.unlink()

        print("File deleted:", file_path.name)

    else:
        print("Deletion cancelled.")


# 2. Delete multiple selected files
def delete_multiple_files(folder_path, file_names):

    folder_path = Path(folder_path)

    for file_name in file_names:

        file_path = folder_path / file_name

        if not file_path.is_file():
            print("File not found:", file_name)
            continue

        confirmation = input(
            f"Delete {file_name}? (yes/no): "
        )

        if confirmation.lower() == "yes":

            file_path.unlink()

            print("Deleted:", file_name)

        else:
            print("Skipped:", file_name)


# 3. Delete files by extension
def delete_files_by_extension(folder_path, extension):

    folder_path = Path(folder_path)

    if not folder_path.is_dir():
        print("Folder not found.")
        return

    files = list(folder_path.glob(f"*{extension}"))

    if not files:
        print("No matching files found.")
        return

    print("\nFiles selected for deletion:")

    for file_path in files:
        print(file_path.name)

    confirmation = input(
        "\nDelete all these files? (yes/no): "
    )

    if confirmation.lower() == "yes":

        for file_path in files:

            if file_path.is_file():
                file_path.unlink()
                print("Deleted:", file_path.name)

    else:
        print("Deletion cancelled.")


# 4. Main execution
if __name__ == "__main__":

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    sample_file = OUTPUT_DIR / "Delete_Test.txt"

    sample_file.write_text(
        "Temporary test file.",
        encoding="utf-8"
    )

    print("\n--- Delete Single File ---")

    delete_file(sample_file)

    print("\nFile deletion operation completed!")
