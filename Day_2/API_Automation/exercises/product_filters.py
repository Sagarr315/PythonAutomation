
import requests

from API_Automation.config.settings import (
    API_BASE_URL,
    REQUEST_TIMEOUT
)


def fetch_products():

    endpoint = f"{API_BASE_URL}/products"

    params = {
        "limit": 5,
        "skip": 10,
        "select": "id,title,price,category"
    }

    try:
        response = requests.get(
            endpoint,
            params=params,
            timeout=REQUEST_TIMEOUT
        )

        print("Status Code:", response.status_code)
        print("Request URL:", response.url)

        response.raise_for_status()

        data = response.json()

        products = data.get("products", [])

        print("\nTotal products:", data.get("total"))
        print("Products received:", len(products))
        print("Skipped records:", data.get("skip"))

        print("\n--- FILTERED PRODUCTS ---")

        for product in products:
            print("ID:", product.get("id"))
            print("Title:", product.get("title"))
            print("Price:", product.get("price"))
            print("Category:", product.get("category"))
            print("-" * 40)

    except requests.exceptions.RequestException as error:
        print("API Error:", error)


if __name__ == "__main__":
    fetch_products()
