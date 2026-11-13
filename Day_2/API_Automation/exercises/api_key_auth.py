
import requests

API_URL = "https://api.weatherapi.com/v1/current.json"

API_KEY = "YOUR_API_KEY"

params = {
    "key": API_KEY,
    "q": "Pune"
}

try:
    response = requests.get(
        API_URL,
        params=params,
        timeout=20
    )

    print("Status Code:", response.status_code)

    data = response.json()

    if response.status_code == 200:
        print("City:", data["location"]["name"])
        print("Temperature:", data["current"]["temp_c"])
        print("Condition:", data["current"]["condition"]["text"])

    else:
        print("API Error:", data.get("error", {}).get("message"))

except requests.exceptions.RequestException as error:
    print("Connection Error:", error)
