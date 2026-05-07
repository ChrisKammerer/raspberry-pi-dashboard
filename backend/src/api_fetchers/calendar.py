from backend.src.api_fetchers.base_fetcher import BaseFetcher
from backend.src.calendar_utils import get_calendar_credentials


class CalendarFetcher(BaseFetcher):
    def __init__(self) -> None:
        super().__init__()
        self.api_key = self.get_env("CALENDAR_API_KEY")

    def update_calendar(self) -> None:
        self.init_db()
        get_calendar_credentials()


def main() -> None:
    CalendarFetcher().update_calendar()
