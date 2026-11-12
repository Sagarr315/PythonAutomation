
import json
from pathlib import Path

import requests

from API_Automation.config.settings import (
    API_BASE_URL,
    REQUEST_TIMEOUT,
    DEFAULT_PRODUCT_LIMIT
)


def fetch_products():

    try:
        # Step 1: Define API endpoint
        endpoint = f"{API_BASE_URL}/products"

        # Step 2: Define query parameters
        params = {
            "limit": DEFAULT_PRODUCT_LIMIT
        }

        # Step 3: Send GET request
        response = requests.get(
            endpoint,
            params=params,
            timeout=REQUEST_TIMEOUT
        )

        # Step 4: Display response information
        print("Status Code:", response.status_code)
        print("Request URL:", response.url)

        # Step 5: Check HTTP errors
        response.raise_for_status()

        # Step 6: Convert JSON response into Python data
        data = response.json()

        # Step 7: Extract products
        products = data.get("products", [])

        print("\n--- API RESPONSE SUMMARY ---")
        print("Total products:", data.get("total"))
        print("Products received:", len(products))
        print("Records skipped:", data.get("skip"))

        # Step 8: Display product information
        print("\n--- PRODUCT DETAILS ---")

        for product in products:

            print("ID:", product.get("id"))
            print("Title:", product.get("title"))
            print("Price:", product.get("price"))
            print("Category:", product.get("category"))
            print("-" * 40)

        # Step 9: Find project output directory
        project_root = Path(__file__).resolve().parents[1]

        output_directory = project_root / "output"

        output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        # Step 10: Save complete API response
        output_file = output_directory / "products_response.json"

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        print("\nAPI data saved successfully!")
        print("File location:", output_file)

    except requests.exceptions.Timeout:
        print("Error: API request timed out.")

    except requests.exceptions.HTTPError as error:
        print("HTTP Error:", error)

    except requests.exceptions.RequestException as error:
        print("API request failed:", error)

    except ValueError as error:
        print("Invalid JSON response:", error)

    except OSError as error:
        print("File operation failed:", error)


if __name__ == "__main__":
    fetch_products()
