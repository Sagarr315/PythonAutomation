
import requests
import time

BASE_URL = "https://dummyjson.com"
TIMEOUT = 20

REQUEST_DELAY = 1


def fetch_products():

    session = requests.Session()

    endpoints = [
        "/products/1",
        "/products/2",
        "/products/3",
        "/products/4",
        "/products/5"
    ]

    try:

        for index, endpoint in enumerate(endpoints):

            # Wait before requests after the first
            if index > 0:
                print(f"\nWaiting {REQUEST_DELAY} second...")
                time.sleep(REQUEST_DELAY)

            url = f"{BASE_URL}{endpoint}"

            response = session.get(
                url,
                timeout=TIMEOUT
            )

            print("\nStatus Code:", response.status_code)

            if response.status_code == 429:

                retry_after = response.headers.get(
                    "Retry-After"
                )

                if retry_after and retry_after.isdigit():
                    wait_time = int(retry_after)
                else:
                    wait_time = 5

                print("Rate limit reached.")
                print("Retry after:", wait_time, "seconds")

                time.sleep(wait_time)

                response = session.get(
                    url,
                    timeout=TIMEOUT
                )

            response.raise_for_status()

            product = response.json()

            print("Product ID:", product.get("id"))
            print("Title:", product.get("title"))
            print("Price:", product.get("price"))

    except requests.exceptions.RequestException as error:
        print("API Error:", error)

    finally:
        session.close()


if __name__ == "__main__":
    fetch_products()
