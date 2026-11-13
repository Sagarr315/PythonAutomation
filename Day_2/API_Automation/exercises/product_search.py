
import requests

BASE_URL = "https://dummyjson.com"
TIMEOUT = 20


def search_products():

    endpoint = f"{BASE_URL}/products/search"

    # Search keyword
    search_keyword = "phone"

    params = {
        "q": search_keyword,
        "limit": 10
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

        print("\n--- SEARCH RESULTS ---")
        print("Search Keyword:", search_keyword)
        print("Total Matching Products:", data.get("total"))
        print("Products Received:", len(products))

        for product in products:

            print("\nProduct ID:", product.get("id"))
            print("Title:", product.get("title"))
            print("Price:", product.get("price"))
            print("Category:", product.get("category"))

        print("\nAPI Search completed!")

    except requests.exceptions.Timeout:
        print("Error: API request timed out.")

    except requests.exceptions.HTTPError as error:
        print("HTTP Error:", error)

    except requests.exceptions.RequestException as error:
        print("API Error:", error)


if __name__ == "__main__":
    search_products()
