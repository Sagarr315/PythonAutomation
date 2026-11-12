from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = BASE_DIR / "Input"
OUTPUT_DIR = BASE_DIR / "Output"
ARCHIVE_DIR = BASE_DIR / "Archive"


# 1. Move a single file
def move_file(source_path, destination_folder):

    source_path = Path(source_path)
    destination_folder = Path(destination_folder)

    if not source_path.is_file():
        print("Source file not found.")
        return

    destination_folder.mkdir(parents=True, exist_ok=True)

    destination_path = destination_folder / source_path.name

    if destination_path.exists():
        print("Destination file already exists.")
        return

    shutil.move(str(source_path), str(destination_path))

    print("File moved:", destination_path.name)


# 2. Move multiple files
def move_multiple_files(source_folder, destination_folder):

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

            shutil.move(str(source_file), str(destination_file))

            print("Moved:", source_file.name)


# 3. Move files by extension
def move_files_by_extension(source_folder, destination_folder, extension):

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

            shutil.move(str(source_file), str(destination_file))

            print("Moved:", source_file.name)


# 4. Main execution
if __name__ == "__main__":

    INPUT_DIR.mkdir(parents=True, exist_ok=True)

    sample_file = INPUT_DIR / "Archive_Sample.txt"

    if not sample_file.exists():
        sample_file.write_text(
            "Sample file for move operation.",
            encoding="utf-8"
        )

    print("\n--- Move Single File ---")
    move_file(sample_file, ARCHIVE_DIR)

    print("\nFile move operations completed!")
