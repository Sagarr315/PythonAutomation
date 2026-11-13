
import requests

from API_Automation.config.settings import (
    API_BASE_URL,
    REQUEST_TIMEOUT
)


def test_http_request():

    endpoint = f"{API_BASE_URL}/products/1"

    # Request headers
    headers = {
        "Accept": "application/json",
        "User-Agent": "Python-Automation-Project"
    }

    try:

        # Send GET request
        response = requests.get(
            endpoint,
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )

        # Request information
        print("========== REQUEST DETAILS ==========")

        print("Request Method:", response.request.method)
        print("Request URL:", response.url)
        print("Request Headers:", response.request.headers)

        # Response information
        print("\n========== RESPONSE DETAILS ==========")

        print("Status Code:", response.status_code)
        print("Response Time:", response.elapsed.total_seconds(), "seconds")
        print("Content Type:", response.headers.get("Content-Type"))

        response.raise_for_status()

        # Convert JSON response to Python dictionary
        product = response.json()

        print("\n========== PRODUCT DATA ==========")

        print("Product ID:", product.get("id"))
        print("Product Name:", product.get("title"))
        print("Price:", product.get("price"))
        print("Category:", product.get("category"))

    except requests.exceptions.Timeout:
        print("Error: Request timed out.")

    except requests.exceptions.HTTPError as error:
        print("HTTP Error:", error)

    except requests.exceptions.RequestException as error:
        print("Request Error:", error)


if __name__ == "__main__":
    test_http_request()
