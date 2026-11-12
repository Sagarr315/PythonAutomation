from pathlib import Path


# 1. Create a single file
def create_single_file(folder_path, file_name, content=""):

    folder = Path(folder_path)
    folder.mkdir(parents=True, exist_ok=True)

    file_path = folder / file_name

    if file_path.exists():
        print("File already exists:", file_path.name)
        return

    file_path.write_text(content, encoding="utf-8")

    print("File created:", file_path.name)


# 2. Create multiple files
def create_multiple_files(folder_path, file_names):

    folder = Path(folder_path)
    folder.mkdir(parents=True, exist_ok=True)

    for file_name in file_names:

        file_path = folder / file_name

        if file_path.exists():
            print("Already exists:", file_name)
            continue

        file_path.write_text("", encoding="utf-8")

        print("File created:", file_name)


# 3. Create files dynamically using a loop
def create_numbered_files(folder_path, prefix, count):

    folder = Path(folder_path)
    folder.mkdir(parents=True, exist_ok=True)

    for number in range(1, count + 1):

        file_name = f"{prefix}_{number:03}.txt"
        file_path = folder / file_name

        if file_path.exists():
            print("Already exists:", file_name)
            continue

        file_path.write_text(
            f"Generated file number: {number}",
            encoding="utf-8"
        )

        print("File created:", file_name)


# 4. Create files with different extensions
def create_files_by_extension(folder_path, extensions):

    folder = Path(folder_path)
    folder.mkdir(parents=True, exist_ok=True)

    for extension in extensions:

        file_name = f"Sample_File{extension}"
        file_path = folder / file_name

        if file_path.exists():
            print("Already exists:", file_name)
            continue

        file_path.write_text(
            "Sample automation data",
            encoding="utf-8"
        )

        print("File created:", file_name)


# 5. Main execution
if __name__ == "__main__":

    output_folder = "Output"

    print("\n--- Single File Creation ---")
    create_single_file(
        output_folder,
        "Report.txt",
        "This is a sample report."
    )

    print("\n--- Multiple File Creation ---")
    create_multiple_files(
        output_folder,
        ["Customer.txt", "Invoice.txt", "Transaction.txt"]
    )

    print("\n--- Numbered File Creation ---")
    create_numbered_files(
        output_folder,
        "Employee",
        5
    )

    print("\n--- Different Extension Creation ---")
    create_files_by_extension(
        output_folder,
        [".txt", ".csv", ".log"]
    )

    print("\nFile creation operations completed!")