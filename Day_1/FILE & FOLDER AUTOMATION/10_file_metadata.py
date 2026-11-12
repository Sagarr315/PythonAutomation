from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "Output"


# 1. Get file name
def get_file_name(file_path):

    file_path = Path(file_path)

    print("File Name:", file_path.name)


# 2. Get file extension
def get_file_extension(file_path):

    file_path = Path(file_path)

    print("File Extension:", file_path.suffix)


# 3. Get file size
def get_file_size(file_path):

    file_path = Path(file_path)

    if not file_path.is_file():
        print("File not found.")
        return

    size_bytes = file_path.stat().st_size

    size_kb = size_bytes / 1024

    size_mb = size_kb / 1024

    print("Size in Bytes:", size_bytes)
    print("Size in KB:", round(size_kb, 2))
    print("Size in MB:", round(size_mb, 2))


# 4. Get file timestamps
def get_file_timestamps(file_path):

    file_path = Path(file_path)

    if not file_path.is_file():
        print("File not found.")
        return

    metadata = file_path.stat()

    modified_time = datetime.fromtimestamp(metadata.st_mtime)
    accessed_time = datetime.fromtimestamp(metadata.st_atime)
    created_time = datetime.fromtimestamp(metadata.st_ctime)

    print("Created/Changed Time:", created_time)
    print("Last Modified:", modified_time)
    print("Last Accessed:", accessed_time)


# 5. Get complete metadata
def get_file_metadata(file_path):

    file_path = Path(file_path)

    if not file_path.is_file():
        print("File not found.")
        return

    metadata = file_path.stat()

    print("\n--- Complete File Metadata ---")

    print("Name:", file_path.name)
    print("Full Path:", file_path.resolve())
    print("Extension:", file_path.suffix)
    print("File Type:", file_path.suffix.upper())
    print("Size:", metadata.st_size, "bytes")

    print(
        "Modified:",
        datetime.fromtimestamp(metadata.st_mtime)
    )

    print(
        "Accessed:",
        datetime.fromtimestamp(metadata.st_atime)
    )

    print(
        "Created/Changed:",
        datetime.fromtimestamp(metadata.st_ctime)
    )


# 6. Main execution
if __name__ == "__main__":

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    sample_file = OUTPUT_DIR / "Metadata_Report.txt"

    if not sample_file.exists():
        sample_file.write_text(
            "Sample metadata file for automation.",
            encoding="utf-8"
        )

    print("\n--- File Name ---")
    get_file_name(sample_file)

    print("\n--- File Extension ---")
    get_file_extension(sample_file)

    print("\n--- File Size ---")
    get_file_size(sample_file)

    print("\n--- File Timestamps ---")
    get_file_timestamps(sample_file)

    print("\n--- Complete Metadata ---")
    get_file_metadata(sample_file)

    print("\nMetadata operations completed!")