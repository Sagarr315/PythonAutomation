
import requests
from pathlib import Path

FILE_URL = "https://dummyjson.com/image/400x200"

TIMEOUT = 30


def download_file():

    try:

        # Project output directory
        project_root = Path(__file__).resolve().parents[1]

        output_directory = project_root / "output"

        output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = output_directory / "sample_image.jpg"

        # Send GET request
        response = requests.get(
            FILE_URL,
            timeout=TIMEOUT
        )

        print("Status Code:", response.status_code)

        response.raise_for_status()

        # Save downloaded file
        with open(output_file, "wb") as file:

            file.write(response.content)

        print("\nFile downloaded successfully!")
        print("File Location:", output_file)
        print("File Size:", len(response.content), "bytes")

    except requests.exceptions.RequestException as error:
        print("API Error:", error)

    except OSError as error:
        print("File Error:", error)


if __name__ == "__main__":
    download_file()
