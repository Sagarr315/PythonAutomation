
import requests
from pathlib import Path

UPLOAD_URL = "https://httpbin.org/post"

TIMEOUT = 30


def upload_file():

    try:

        # Locate downloaded file
        project_root = Path(__file__).resolve().parents[1]

        file_path = project_root / "output" / "sample_image.jpg"

        if not file_path.exists():

            print("File not found:", file_path)
            return

        # Open file in binary mode
        with open(file_path, "rb") as file:

            files = {
                "file": (
                    file_path.name,
                    file,
                    "image/jpeg"
                )
            }

            response = requests.post(
                UPLOAD_URL,
                files=files,
                timeout=TIMEOUT
            )

        print("Status Code:", response.status_code)

        response.raise_for_status()

        data = response.json()

        print("\n--- UPLOAD RESPONSE ---")

        uploaded_file = data.get("files", {})

        print("Uploaded File Name:", file_path.name)
        print("Server Received File:", bool(uploaded_file))
        print("File Size:", file_path.stat().st_size, "bytes")

        print("\nFile upload request completed!")

    except requests.exceptions.RequestException as error:
        print("API Error:", error)

    except OSError as error:
        print("File Error:", error)


if __name__ == "__main__":
    upload_file()
