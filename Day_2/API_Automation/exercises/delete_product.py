
import requests

from API_Automation.config.settings import (
    API_BASE_URL,
    REQUEST_TIMEOUT
)


def delete_product():

    product_id = 1

    endpoint = f"{API_BASE_URL}/products/{product_id}"

    try:
        response = requests.delete(
            endpoint,
            timeout=REQUEST_TIMEOUT
        )

        print("Status Code:", response.status_code)
        print("Request URL:", response.url)

        response.raise_for_status()

        deleted_data = response.json()

        print("\n--- DELETE RESPONSE ---")
        print("Product ID:", deleted_data.get("id"))
        print("Product Title:", deleted_data.get("title"))
        print("Is Deleted:", deleted_data.get("isDeleted"))
        print("Deleted On:", deleted_data.get("deletedOn"))

        print("\nDELETE request completed successfully!")

    except requests.exceptions.RequestException as error:
        print("API Error:", error)


if __name__ == "__main__":
    delete_product()
