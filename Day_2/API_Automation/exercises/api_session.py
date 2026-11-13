
import requests

BASE_URL = "https://dummyjson.com"
TIMEOUT = 20


def fetch_products_with_session():

    # Create reusable session
    session = requests.Session()

    # Set common headers
    session.headers.update({
        "Accept": "application/json",
        "User-Agent": "Python-Automation-Project"
    })

    endpoints = [
        "/products/1",
        "/products/2",
        "/products/3"
    ]

    try:

        for endpoint in endpoints:

            url = f"{BASE_URL}{endpoint}"

            response = session.get(
                url,
                timeout=TIMEOUT
            )

            response.raise_for_status()

            product = response.json()

            print("\nProduct ID:", product.get("id"))
            print("Title:", product.get("title"))
            print("Price:", product.get("price"))

        print("\nAll API requests completed!")

    except requests.exceptions.RequestException as error:
        print("API Error:", error)

    finally:
        # Close session and release resources
        session.close()


if __name__ == "__main__":
    fetch_products_with_session()
