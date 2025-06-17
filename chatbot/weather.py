import requests
import os

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "demo-key")  # Replace with real key


def fetch_weather_alert(location):
    # Dummy endpoint, replace with real API (e.g., OpenWeatherMap)
    try:
        url = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            condition = data['current']['condition']['text']
            return condition
        return None
    except Exception:
        return None