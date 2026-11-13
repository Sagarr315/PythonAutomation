
import requests

BASE_URL = "https://dummyjson.com"
TIMEOUT = 20

LIMIT = 10


def fetch_all_products():

    skip = 0
    all_products = []

    try:

        while True:

            endpoint = f"{BASE_URL}/products"

            params = {
                "limit": LIMIT,
                "skip": skip
            }

            response = requests.get(
                endpoint,
                params=params,
                timeout=TIMEOUT
            )

            response.raise_for_status()

            data = response.json()

            products = data.get("products", [])

            if not products:
                break

            all_products.extend(products)

            print(
                f"Fetched {len(products)} products "
                f"| Total collected: {len(all_products)}"
            )

            skip += LIMIT

            if len(all_products) >= data.get("total", 0):
                break

        print("\n--- FINAL SUMMARY ---")
        print("Total products fetched:", len(all_products))

        for product in all_products[:5]:
            print(
                product.get("id"),
                product.get("title"),
                product.get("price")
            )

    except requests.exceptions.RequestException as error:
        print("API Error:", error)


if __name__ == "__main__":
    fetch_all_products()
