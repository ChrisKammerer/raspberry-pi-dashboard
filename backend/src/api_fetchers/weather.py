import requests
import time

from backend.config import WEATHER_LAT, WEATHER_LON
from backend.src.api_fetchers.base_fetcher import BaseFetcher
from backend.src.db_utils import upsert_cache


class WeatherFetcher(BaseFetcher):
    BASE_URL = "https://api.weatherapi.com/v1"
    CACHE_TTL_MINUTES = 30

    def __init__(self) -> None:
        super().__init__()
        self.api_key = self.get_env("WEATHER_API_KEY", required=True)

    def update_weather(self) -> None:
        self.init_db()

        current_data = self.get_current_weather()
        hourly_data = self.get_next_3_hours()

        updated_at = self.now_utc()
        expires_at = self.expires_at(self.CACHE_TTL_MINUTES)

        upsert_cache("current_weather", current_data, updated_at, expires_at)
        upsert_cache("hourly_weather", hourly_data, updated_at, expires_at)

    def get_current_weather(self):
        params = {"key": self.api_key, "q": f"{WEATHER_LAT},{WEATHER_LON}"}
        response = requests.get(f"{self.BASE_URL}/current.json", params=params).json()
        return {
            "temp": response["current"]["temp_f"],
            "condition": response["current"]["condition"]["text"],
            "icon": response["current"]["condition"]["icon"],
            "code": response["current"]["condition"]["code"],
            "wind_speed": response["current"]["wind_mph"],
            "humidity": response["current"]["humidity"],
            "precipitation": response["current"]["precip_in"],
        }

    def get_forecast_weather(self, days: int):
        params = {
            "key": self.api_key,
            "q": f"{WEATHER_LAT},{WEATHER_LON}",
            "days": days,
        }
        response = requests.get(f"{self.BASE_URL}/forecast.json", params=params)
        return response.json()

    def get_next_3_hours(self):
        hourly_data = self.get_forecast_weather(days=2)

        hours = hourly_data["forecast"]["forecastday"][0]["hour"]
        current_epoch = time.time()
        next_3_hours = [hour for hour in hours if hour["time_epoch"] > current_epoch]
        next_3_hours = next_3_hours[:3]

        return [
            {
                "time": hour["time"],
                "condition": hour["condition"]["text"],
                "icon": hour["condition"]["icon"],
                "code": hour["condition"]["code"],
                "temp": hour["temp_f"],
                "precipitation": hour["precip_in"],
            }
            for hour in next_3_hours
        ]


def main() -> None:
    WeatherFetcher().update_weather()
