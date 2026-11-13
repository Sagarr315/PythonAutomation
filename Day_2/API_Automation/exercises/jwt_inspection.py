
import requests
import json
import base64


BASE_URL = "https://dummyjson.com"
TIMEOUT = 20


def decode_jwt_part(part):

    # Convert Base64 URL-safe data
    padding = "=" * (-len(part) % 4)

    decoded_bytes = base64.urlsafe_b64decode(
        part + padding
    )

    return json.loads(decoded_bytes)


def inspect_jwt():

    login_url = f"{BASE_URL}/auth/login"

    credentials = {
        "username": "emilys",
        "password": "emilyspass"
    }

    try:

        # Step 1: Login
        response = requests.post(
            login_url,
            json=credentials,
            timeout=TIMEOUT
        )

        response.raise_for_status()

        login_data = response.json()

        token = login_data.get("accessToken")

        if not token:
            print("JWT token not received.")
            return

        print("Login successful!")

        # Step 2: Split JWT into three parts
        parts = token.split(".")

        if len(parts) != 3:
            print("Token does not have the standard JWT structure.")
            return

        header = decode_jwt_part(parts[0])
        payload = decode_jwt_part(parts[1])

        # Step 3: Display decoded information
        print("\n--- JWT HEADER ---")
        print(json.dumps(header, indent=4))

        print("\n--- JWT PAYLOAD ---")
        print(json.dumps(payload, indent=4))

        print("\n--- JWT STRUCTURE ---")
        print("Header: Present")
        print("Payload: Present")
        print("Signature: Present")

        print("\nNote: This program decodes the token.")
        print("It does NOT verify the signature.")

    except requests.exceptions.RequestException as error:
        print("API Error:", error)

    except (ValueError, TypeError) as error:
        print("JWT decoding error:", error)


if __name__ == "__main__":
    inspect_jwt()
