import requests

from backend.src.api_fetchers.base_fetcher import BaseFetcher
from backend.src.db_utils import upsert_cache
from datetime import datetime, timedelta
from backend.config import TIMEZONE_OFFSET

class SportsFetcher(BaseFetcher):
    CACHE_TTL_MINUTES = 30
    TEAM_ID = "16" # Cubs

    
    def __init__(self) -> None:
        super().__init__()

    def get_events(self) -> None:
        self.init_db()

        response = requests.get("https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard").json()

        event = [event for event in response["events"] for competitor in event["competitions"][0]["competitors"] if competitor["id"] == self.TEAM_ID]
        data = {
            "status": "No game today",
            "score": "",
            "time": "",
        }
        if event:
            data["status"] = event[0]["shortName"]
            data["score"] = f"{event[0]['competitions'][0]['competitors'][1]['score']} - {event[0]['competitions'][0]['competitors'][0]['score']}"
            raw_time = event[0]["date"]
            display_time = datetime.fromisoformat(raw_time[:-1]) + timedelta(hours=TIMEZONE_OFFSET)
            data["time"] = display_time.strftime("%I:%M %p")

        updated_at = self.now_utc()
        expires_at = self.expires_at(self.CACHE_TTL_MINUTES)

        upsert_cache("game-score", data, updated_at, expires_at)


def main() -> None:
    SportsFetcher().get_events()    
