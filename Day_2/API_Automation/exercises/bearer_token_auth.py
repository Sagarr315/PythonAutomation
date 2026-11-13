
import requests

BASE_URL = "https://dummyjson.com"

TIMEOUT = 20


def authenticate():

    login_url = f"{BASE_URL}/auth/login"

    credentials = {
        "username": "emilys",
        "password": "emilyspass"
    }

    try:
        # Step 1: Login and obtain token
        login_response = requests.post(
            login_url,
            json=credentials,
            timeout=TIMEOUT
        )

        print("Login Status:", login_response.status_code)

        login_response.raise_for_status()

        login_data = login_response.json()

        access_token = login_data.get("accessToken")

        if not access_token:
            print("Access token not received.")
            return

        print("Authentication successful!")

        # Step 2: Create Bearer Token header
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        # Step 3: Access protected user endpoint
        profile_url = f"{BASE_URL}/auth/me"

        profile_response = requests.get(
            profile_url,
            headers=headers,
            timeout=TIMEOUT
        )

        print("\nProfile Status:", profile_response.status_code)

        profile_response.raise_for_status()

        user_data = profile_response.json()

        print("\n--- AUTHENTICATED USER ---")
        print("ID:", user_data.get("id"))
        print("Username:", user_data.get("username"))
        print("Email:", user_data.get("email"))

    except requests.exceptions.RequestException as error:
        print("API Error:", error)


if __name__ == "__main__":
    authenticate()
