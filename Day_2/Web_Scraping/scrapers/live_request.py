
from pathlib import Path

import requests


# Website URL
WEBSITE_URL = "https://books.toscrape.com/"


def fetch_website():

    try:
        # Step 1: Configure request headers
        headers = {
            "User-Agent": "Mozilla/5.0 PythonWebScraper/1.0"
        }

        # Step 2: Send HTTP GET request
        response = requests.get(
            WEBSITE_URL,
            headers=headers,
            timeout=20
        )

        # Step 3: Display response details
        print("Status Code:", response.status_code)
        print("Response URL:", response.url)

        # Step 4: Check HTTP response
        response.raise_for_status()

        # Step 5: Display response headers
        print("\n--- RESPONSE HEADERS ---")

        print(
            "Content Type:",
            response.headers.get("Content-Type")
        )

        print(
            "Content Length:",
            response.headers.get("Content-Length")
        )

        # Step 6: Get HTML content
        html_content = response.text

        print("\n--- HTML RESPONSE ---")

        print("HTML length:", len(html_content))

        # Step 7: Display first 1000 characters
        print("\nFirst 1000 characters:")

        print(html_content[:1000])

        # Step 8: Find project root directory
        project_root = Path(__file__).resolve().parents[1]

        # Step 9: Create output directory
        output_directory = project_root / "output"

        output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        # Step 10: Define output file
        output_file = output_directory / "website_response.html"

        # Step 11: Save HTML content
        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(html_content)

        print("\nHTML successfully saved!")
        print("File location:", output_file)

    except requests.exceptions.Timeout:

        print("Error: Website request timed out.")

    except requests.exceptions.HTTPError as error:

        print("HTTP Error:", error)

    except requests.exceptions.RequestException as error:

        print("Request failed:", error)

    except OSError as error:

        print("File operation failed:", error)


if __name__ == "__main__":
    fetch_website()
