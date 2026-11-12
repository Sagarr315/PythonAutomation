
import requests

from API_Automation.config.settings import (
    API_BASE_URL,
    REQUEST_TIMEOUT
)


def update_product():

    endpoint = f"{API_BASE_URL}/products/1"

    updated_data = {
        "price": 75000
    }

    try:
        response = requests.patch(
            endpoint,
            json=updated_data,
            timeout=REQUEST_TIMEOUT
        )

        print("Status Code:", response.status_code)

        response.raise_for_status()

        data = response.json()

        print("\n--- PATCH RESPONSE ---")
        print("ID:", data.get("id"))
        print("Title:", data.get("title"))
        print("Updated Price:", data.get("price"))

    except requests.exceptions.RequestException as error:
        print("API Error:", error)


if __name__ == "__main__":
    update_product()
