from pathlib import Path


def list_files(folder_path):

    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(
            f"Folder not found: {folder}"
        )

    if not folder.is_dir():
        raise NotADirectoryError(folder)

    files = [
        file for file in folder.iterdir()
        if file.is_file()
    ]

    return files