from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = BASE_DIR / "Input"
OUTPUT_DIR = BASE_DIR / "Output"


# 1. Copy a single file
def copy_file(source_path, destination_folder):

    source_path = Path(source_path)
    destination_folder = Path(destination_folder)

    if not source_path.is_file():
        print("Source file not found:", source_path)
        return

    destination_folder.mkdir(parents=True, exist_ok=True)

    destination_path = destination_folder / source_path.name

    if destination_path.exists():
        print("Destination file already exists:", destination_path.name)
        return

    shutil.copy2(source_path, destination_path)

    print("File copied:", destination_path.name)


# 2. Copy multiple files
def copy_multiple_files(source_folder, destination_folder):

    source_folder = Path(source_folder)
    destination_folder = Path(destination_folder)

    if not source_folder.is_dir():
        print("Source folder not found.")
        return

    destination_folder.mkdir(parents=True, exist_ok=True)

    for source_file in source_folder.iterdir():

        if source_file.is_file():

            destination_file = destination_folder / source_file.name

            if destination_file.exists():
                print("Already exists:", source_file.name)
                continue

            shutil.copy2(source_file, destination_file)

            print("Copied:", source_file.name)


# 3. Copy files by extension
def copy_files_by_extension(source_folder, destination_folder, extension):

    source_folder = Path(source_folder)
    destination_folder = Path(destination_folder)

    if not source_folder.is_dir():
        print("Source folder not found.")
        return

    destination_folder.mkdir(parents=True, exist_ok=True)

    for source_file in source_folder.glob(f"*{extension}"):

        if source_file.is_file():

            destination_file = destination_folder / source_file.name

            if destination_file.exists():
                print("Already exists:", source_file.name)
                continue

            shutil.copy2(source_file, destination_file)

            print("Copied:", source_file.name)


# 4. Main execution
if __name__ == "__main__":

    # Create a source sample file
    sample_file = INPUT_DIR / "Invoice_001.txt"
    INPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not sample_file.exists():
        sample_file.write_text(
            "Invoice Number: INV001\nAmount: 5000",
            encoding="utf-8"
        )

    print("\n--- Copy Single File ---")
    copy_file(sample_file, OUTPUT_DIR)

    print("\n--- Copy Multiple Files ---")
    copy_multiple_files(INPUT_DIR, OUTPUT_DIR)

    print("\n--- Copy CSV Files ---")
    copy_files_by_extension(INPUT_DIR, OUTPUT_DIR, ".csv")

    print("\nFile copy operations completed!")
