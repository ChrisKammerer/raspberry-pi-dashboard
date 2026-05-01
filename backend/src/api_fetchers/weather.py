import requests

from config import WEATHER_API_KEY, WEATHER_LAT, WEATHER_LON, WEATHER_UNITS
from src.db import init_db, upsert_cache, get_cache
from datetime import datetime, timezone, timedelta

KEY = "weather"

def update_weather():
    init_db()

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={WEATHER_LAT}&lon={WEATHER_LON}&units={WEATHER_UNITS}&appid={WEATHER_API_KEY}"
    data = requests.get(url).json()

    parsed_data = parse_raw_weather_data(data)

    updated_at = datetime.now(timezone.utc)
    expires_at = updated_at + timedelta(minutes=30)
    upsert_cache(KEY, parsed_data, updated_at, expires_at)

def parse_raw_weather_data(data):
    parsed_data = {
        "id": data["weather"][0]["id"],
        "description": data["weather"][0]["main"],
        "icon_id": data["weather"][0]["icon"],
        "temp_now": data["main"]["temp"],
        "temp_min": data["main"]["temp_min"],
        "temp_max": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"],
        "city": data["name"]
    }
    return parsed_data

