from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


# 1. Create a folder
def create_folder(folder_path):

    folder_path = Path(folder_path)

    folder_path.mkdir(parents=True, exist_ok=True)

    print("Folder created or already exists:", folder_path.name)


# 2. List folders
def list_folders(folder_path):

    folder_path = Path(folder_path)

    if not folder_path.is_dir():
        print("Folder not found.")
        return

    print("\nAvailable folders:")

    for item in folder_path.iterdir():

        if item.is_dir():
            print(item.name)


# 3. List files and folders
def list_folder_contents(folder_path):

    folder_path = Path(folder_path)

    if not folder_path.is_dir():
        print("Folder not found.")
        return

    print("\nFolder contents:")

    for item in folder_path.iterdir():

        if item.is_file():
            print("FILE:", item.name)

        elif item.is_dir():
            print("FOLDER:", item.name)


# 4. Check whether a folder exists
def check_folder(folder_path):

    folder_path = Path(folder_path)

    if folder_path.is_dir():
        print("Folder exists:", folder_path.name)

    else:
        print("Folder does not exist:", folder_path.name)


# 5. Rename a folder
def rename_folder(folder_path, new_name):

    folder_path = Path(folder_path)

    if not folder_path.is_dir():
        print("Folder not found.")
        return

    new_path = folder_path.with_name(new_name)

    if new_path.exists():
        print("New folder name already exists.")
        return

    folder_path.rename(new_path)

    print("Folder renamed:", new_name)


# 6. Delete an empty folder
def delete_empty_folder(folder_path):

    folder_path = Path(folder_path)

    if not folder_path.is_dir():
        print("Folder not found.")
        return

    try:
        folder_path.rmdir()
        print("Empty folder deleted:", folder_path.name)

    except OSError:
        print("Folder is not empty. No deletion performed.")


# 7. Main execution
if __name__ == "__main__":

    print("\n--- Create Folder ---")
    create_folder(BASE_DIR / "Test_Folder")

    print("\n--- List Folders ---")
    list_folders(BASE_DIR)

    print("\n--- List All Contents ---")
    list_folder_contents(BASE_DIR)

    print("\n--- Check Folder ---")
    check_folder(BASE_DIR / "Input")

    print("\n--- Rename Folder ---")
    # Uncomment to test:
    # rename_folder(BASE_DIR / "Test_Folder", "Renamed_Folder")

    print("\n--- Delete Empty Folder ---")
    # Uncomment to test:
    # delete_empty_folder(BASE_DIR / "Test_Folder")

    print("\nFolder management completed!")
