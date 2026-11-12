
import requests

from API_Automation.config.settings import (
    API_BASE_URL,
    REQUEST_TIMEOUT
)


def create_product():

    endpoint = f"{API_BASE_URL}/products/add"

    # Data we want to send to the API
    product_data = {
        "title": "Automation Practice Laptop",
        "price": 55000,
        "category": "electronics"
    }

    try:
        # Send POST request with JSON body
        response = requests.post(
            endpoint,
            json=product_data,
            timeout=REQUEST_TIMEOUT
        )

        print("Status Code:", response.status_code)
        print("Request URL:", response.url)

        response.raise_for_status()

        # Convert JSON response into Python dictionary
        created_product = response.json()

        print("\n--- CREATED PRODUCT RESPONSE ---")

        print("Product ID:", created_product.get("id"))
        print("Title:", created_product.get("title"))
        print("Price:", created_product.get("price"))
        print("Category:", created_product.get("category"))

        print("\nPOST request completed successfully!")

    except requests.exceptions.RequestException as error:
        print("API Error:", error)


if __name__ == "__main__":
    create_product()
