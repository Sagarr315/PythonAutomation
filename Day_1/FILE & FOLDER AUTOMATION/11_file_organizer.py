
from pathlib import Path
import shutil
from datetime import datetime


# ==========================================
# 1. PROJECT CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = BASE_DIR / "Input"
OUTPUT_DIR = BASE_DIR / "Output"

LOG_FILE = OUTPUT_DIR / "Automation_Log.txt"


# File categories
FILE_CATEGORIES = {
    ".pdf": "PDF",
    ".txt": "Text",
    ".csv": "CSV",
    ".docx": "Documents",
    ".doc": "Documents",
    ".xlsx": "Excel",
    ".xls": "Excel",
    ".png": "Images",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".gif": "Images",
    ".zip": "Archives",
    ".log": "Logs"
}


# ==========================================
# 2. CREATE REQUIRED FOLDERS
# ==========================================

def create_required_folders():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    categories = set(FILE_CATEGORIES.values())
    categories.add("Other")

    for category in categories:

        folder = OUTPUT_DIR / category

        folder.mkdir(parents=True, exist_ok=True)

    print("Required folders created successfully.")


# ==========================================
# 3. GET INPUT FILES
# ==========================================

def get_input_files():

    if not INPUT_DIR.is_dir():

        raise FileNotFoundError(
            f"Input folder not found: {INPUT_DIR}"
        )

    files = [
        file for file in INPUT_DIR.iterdir()
        if file.is_file()
    ]

    print(f"Total files found: {len(files)}")

    return files


# ==========================================
# 4. IDENTIFY FILE CATEGORY
# ==========================================

def identify_category(file_path):

    extension = file_path.suffix.lower()

    category = FILE_CATEGORIES.get(
        extension,
        "Other"
    )

    return category


# ==========================================
# 5. GENERATE SAFE DESTINATION NAME
# ==========================================

def get_unique_destination(destination_path):

    if not destination_path.exists():
        return destination_path

    counter = 1

    while True:

        new_name = (
            f"{destination_path.stem}_{counter}"
            f"{destination_path.suffix}"
        )

        new_path = destination_path.with_name(new_name)

        if not new_path.exists():
            return new_path

        counter += 1


# ==========================================
# 6. COPY FILES INTO CATEGORIES
# ==========================================

def organize_files(files):

    successful = 0
    failed = 0

    for source_file in files:

        try:

            category = identify_category(source_file)

            destination_folder = OUTPUT_DIR / category

            destination_folder.mkdir(
                parents=True,
                exist_ok=True
            )

            destination_file = (
                destination_folder / source_file.name
            )

            destination_file = get_unique_destination(
                destination_file
            )

            shutil.copy2(
                source_file,
                destination_file
            )

            # Verify copied file
            if (
                destination_file.is_file()
                and destination_file.stat().st_size
                == source_file.stat().st_size
            ):

                successful += 1

                print(
                    f"SUCCESS: {source_file.name}"
                    f" -> {category}"
                )

                write_log(
                    f"SUCCESS: {source_file.name}"
                    f" copied to {category}"
                )

            else:

                failed += 1

                print("VERIFICATION FAILED:", source_file.name)

                write_log(
                    f"VERIFICATION FAILED: {source_file.name}"
                )

        except OSError as error:

            failed += 1

            print(
                f"ERROR processing {source_file.name}: {error}"
            )

            write_log(
                f"ERROR: {source_file.name}: {error}"
            )

    return successful, failed


# ==========================================
# 7. WRITE EXECUTION LOG
# ==========================================

def write_log(message):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(LOG_FILE, "a", encoding="utf-8") as file:

        file.write(
            f"[{timestamp}] {message}\n"
        )


# ==========================================
# 8. DISPLAY FINAL SUMMARY
# ==========================================

def display_summary(total, successful, failed):

    print("\n================================")
    print("       AUTOMATION SUMMARY")
    print("================================")

    print("Total Files:", total)
    print("Successful:", successful)
    print("Failed:", failed)

    print("Log File:", LOG_FILE)

    print("================================")


# ==========================================
# 9. MAIN BOT EXECUTION
# ==========================================

def main():

    print("\n================================")
    print("     FILE ORGANIZER BOT")
    print("================================")

    try:

        # Step 1: Create destination folders
        print("\nSTEP 1: Creating folders")

        create_required_folders()

        # Step 2: Scan input folder
        print("\nSTEP 2: Scanning input folder")

        files = get_input_files()

        total = len(files)

        if total == 0:

            print("No files available for processing.")

            return

        # Step 3: Organize files
        print("\nSTEP 3: Organizing files")

        successful, failed = organize_files(files)

        # Step 4: Final summary
        print("\nSTEP 4: Generating summary")

        display_summary(
            total,
            successful,
            failed
        )

        write_log(
            f"BOT COMPLETED | Total: {total} | "
            f"Successful: {successful} | Failed: {failed}"
        )

        print("\nBOT EXECUTION COMPLETED!")

    except Exception as error:

        print("\nBOT EXECUTION FAILED:", error)

        write_log(f"BOT FAILED: {error}")


# ==========================================
# 10. APPLICATION ENTRY POINT
# ==========================================

if __name__ == "__main__":

    main()
