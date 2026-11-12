import subprocess
import shutil
import os

import psutil


def launch_application(application_name):
    applications = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "explorer": "explorer.exe",
    }

    executable = applications.get(application_name.lower())

    if executable is None:
        print("Unsupported application:", application_name)
        return

    executable_path = shutil.which(executable)

    if executable_path is None:
        print("Application not found:", executable)
        return

    process = subprocess.Popen([executable_path])

    print(f"{application_name} launched successfully.")
    print("Process ID:", process.pid)


def open_folder(folder_path):
    folder_path = os.path.abspath(folder_path)

    if not os.path.isdir(folder_path):
        print("Folder does not exist:", folder_path)
        return

    os.startfile(folder_path)
    print("Folder opened:", folder_path)


def list_running_applications():
    print("\n--- Running Applications ---")

    for process in psutil.process_iter(["pid", "name"]):
        try:
            name = process.info["name"]

            if name:
                print(process.info["pid"], name)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue


if __name__ == "__main__":
    launch_application("notepad")
    list_running_applications()