from backend.src.api_fetchers.base_fetcher import BaseFetcher
from backend.src.calendar_utils import get_calendar_credentials
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from backend.src.db_utils import init_db, upsert_cache


class CalendarFetcher(BaseFetcher):
    def __init__(self) -> None:
        super().__init__()
        self.creds_path = self.get_env("GOOGLE_CREDENTIALS_PATH", required=True)
        self.calendar_id = self.get_env("CALENDAR_ID", required=True)

    def update_calendar(self) -> None:
        self.init_db()

        creds = get_calendar_credentials(self.creds_path)
        events = self.get_calendar_events(creds, self.calendar_id)
        updated_at = self.now_utc()
        expires_at = self.expires_at(60)  # Cache for 60 minutes

        upsert_cache("calendar_events", events, updated_at, expires_at)

    def get_calendar_events(self, creds, calendar_id, max_results=10):
        try:
            service = build("calendar", "v3", credentials=creds)
            now = self.now_utc().isoformat()
            events_results = (
                service.events()
                .list(
                    calendarId=calendar_id,
                    timeMin=now,
                    maxResults=max_results,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_results.get("items", [])
            return events
        except HttpError as error:
            return []


def main() -> None:
    CalendarFetcher().update_calendar()
