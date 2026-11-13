
import requests

BASE_URL = "https://dummyjson.com"
TIMEOUT = 20


def fetch_filtered_products():

    # API endpoint for smartphones
    endpoint = f"{BASE_URL}/products/category/smartphones"

    # Filtering and sorting parameters
    params = {
        "limit": 10,
        "sortBy": "price",
        "order": "asc"
    }

    try:

        response = requests.get(
            endpoint,
            params=params,
            timeout=TIMEOUT
        )

        print("Status Code:", response.status_code)
        print("Request URL:", response.url)

        response.raise_for_status()

        data = response.json()

        products = data.get("products", [])

        print("\n--- FILTERED AND SORTED PRODUCTS ---")

        print("Total Available:", data.get("total"))
        print("Products Received:", len(products))

        for product in products:

            print("\nProduct ID:", product.get("id"))
            print("Title:", product.get("title"))
            print("Category:", product.get("category"))
            print("Price:", product.get("price"))

        print("\nFiltering and sorting completed!")

    except requests.exceptions.RequestException as error:
        print("API Error:", error)


if __name__ == "__main__":
    fetch_filtered_products()
