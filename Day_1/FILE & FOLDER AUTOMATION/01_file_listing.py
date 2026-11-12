from file_utils import list_files


input_folder = "Input"

try:

    files = list_files(input_folder)

    print("\nFiles available in Input folder:")

    for file in files:
        print(file.name)

    print("\nTotal files:", len(files))

except FileNotFoundError as error:
    print("Error:", error)

except NotADirectoryError as error:
    print("Error:", error)