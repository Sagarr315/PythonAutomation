
import requests
import time

BASE_URL = "https://dummyjson.com"
TIMEOUT = (5, 20)

MAX_RETRIES = 3


def fetch_product():

    endpoint = f"{BASE_URL}/products/1"

    for attempt in range(1, MAX_RETRIES + 1):

        try:
            print(f"\nAttempt {attempt}")

            response = requests.get(
                endpoint,
                timeout=TIMEOUT
            )

            response.raise_for_status()

            product = response.json()

            print("\nAPI Request Successful!")
            print("Product ID:", product.get("id"))
            print("Title:", product.get("title"))
            print("Price:", product.get("price"))

            return

        except requests.exceptions.Timeout:
            print("Request timed out.")

        except requests.exceptions.ConnectionError:
            print("Connection failed.")

        except requests.exceptions.HTTPError as error:

            status_code = error.response.status_code

            # Retry only temporary server errors
            if status_code not in (429, 500, 502, 503, 504):
                print("Non-retryable HTTP error:", error)
                return

            print("Temporary HTTP error:", status_code)

        except requests.exceptions.RequestException as error:
            print("Request failed:", error)
            return

        # Exponential backoff
        if attempt < MAX_RETRIES:

            wait_time = 2 ** (attempt - 1)

            print(f"Retrying after {wait_time} seconds...")

            time.sleep(wait_time)

    print("\nMaximum retry attempts reached.")


if __name__ == "__main__":
    fetch_product()
