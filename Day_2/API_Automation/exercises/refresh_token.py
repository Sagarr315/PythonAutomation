
import requests

BASE_URL = "https://dummyjson.com"
TIMEOUT = 20


def refresh_access_token():

    try:
        # STEP 1: Login
        login_url = f"{BASE_URL}/auth/login"

        credentials = {
            "username": "emilys",
            "password": "emilyspass"
        }

        login_response = requests.post(
            login_url,
            json=credentials,
            timeout=TIMEOUT
        )

        login_response.raise_for_status()

        login_data = login_response.json()

        access_token = login_data.get("accessToken")
        refresh_token = login_data.get("refreshToken")

        if not refresh_token:
            print("Refresh token not received.")
            return

        print("Login successful!")
        print("Access token received:", bool(access_token))
        print("Refresh token received:", bool(refresh_token))

        # STEP 2: Refresh the access token
        refresh_url = f"{BASE_URL}/auth/refresh"

        refresh_payload = {
            "refreshToken": refresh_token,
            "expiresInMins": 30
        }

        refresh_response = requests.post(
            refresh_url,
            json=refresh_payload,
            timeout=TIMEOUT
        )

        print("\nRefresh Status:", refresh_response.status_code)

        refresh_response.raise_for_status()

        refreshed_data = refresh_response.json()

        new_access_token = refreshed_data.get("accessToken")

        if not new_access_token:
            print("New access token not received.")
            return

        print("New access token received:", bool(new_access_token))

        # STEP 3: Access protected API using new token
        profile_url = f"{BASE_URL}/auth/me"

        headers = {
            "Authorization": f"Bearer {new_access_token}"
        }

        profile_response = requests.get(
            profile_url,
            headers=headers,
            timeout=TIMEOUT
        )

        print("\nProfile Status:", profile_response.status_code)

        profile_response.raise_for_status()

        profile_data = profile_response.json()

        print("\n--- USER PROFILE ---")
        print("Username:", profile_data.get("username"))
        print("Email:", profile_data.get("email"))

        print("\nToken refresh workflow completed!")

    except requests.exceptions.HTTPError as error:
        print("HTTP Error:", error)

    except requests.exceptions.RequestException as error:
        print("Connection Error:", error)


if __name__ == "__main__":
    refresh_access_token()
