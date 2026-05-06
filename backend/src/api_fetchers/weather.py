import requests
import time

from backend.config import WEATHER_API_KEY, WEATHER_LAT, WEATHER_LON, WEATHER_UNITS
from backend.src.db import init_db, upsert_cache, get_cache
from datetime import datetime, timezone, timedelta

BASE_URL = "https://api.weatherapi.com/v1"

def update_weather():
    init_db()

    current_data = get_current_weather()
    hourly_data = get_next_3_hours()

    updated_at = datetime.now(timezone.utc)
    expires_at = updated_at + timedelta(minutes=30)

    upsert_cache("current_weather", current_data, updated_at, expires_at)
    upsert_cache("hourly_weather", hourly_data, updated_at, expires_at)



def get_current_weather():
    params = {
        "key": WEATHER_API_KEY,
        "q": f"{WEATHER_LAT},{WEATHER_LON}"
    }
    response = requests.get(f"{BASE_URL}/current.json", params=params).json()
    parsed_data = {
        "temp": response["current"]["temp_f"],
        "condition": response["current"]["condition"]["text"],
        "icon": response["current"]["condition"]["icon"],
        "code": response["current"]["condition"]["code"],
        "wind_speed": response["current"]["wind_mph"],
        "humidity": response["current"]["humidity"],
        "precipitation": response["current"]["precip_in"]
    }
    return parsed_data


def get_forecast_weather(days):
    params = {
        "key": WEATHER_API_KEY,
        "q": f"{WEATHER_LAT},{WEATHER_LON}",
        "days": days
    }
    response = requests.get(f"{BASE_URL}/forecast.json", params=params)
    return response.json()


def get_next_3_hours():
    hourly_data = get_forecast_weather(days=2)

    hours = hourly_data["forecast"]["forecastday"][0]["hour"]
    current_epoch = time.time()
    next_3_hours = []
    for hour in hours:
        if hour["time_epoch"] > current_epoch:
            next_3_hours.append(hour)
    next_3_hours = next_3_hours[1:4]

    parsed_data = []
    for hour in next_3_hours:
        parsed_data.append(
            {
                "time": hour["time"],
                "condition": hour["condition"]["text"],
                "icon": hour["condition"]["icon"],
                "code": hour["condition"]["code"],
                "temp": hour["temp_f"],
                "precipitation": hour["precip_in"]
            }
        )

    return parsed_data


def main():
    update_weather()