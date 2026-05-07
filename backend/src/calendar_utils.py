import pickle
import logging

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from pathlib import Path


def get_calendar_credentials(creds_path):
    creds = None
    try:
        token_filename = "backend/token.pickle"

        token_file = Path(token_filename).resolve()

        if token_file.exists():
            with open(token_filename, "rb") as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logging.info("Refreshing calendar credentials...")
                creds.refresh(Request())
            else:
                creds_file = Path(creds_path).resolve()
                if not creds_file.exists():
                    logging.error(
                        f"Calendar credentials file not found at {creds_file}"
                    )
                    return None
                flow = InstalledAppFlow.from_client_secrets_file(
                    creds_file,
                    scopes=["https://www.googleapis.com/auth/calendar.readonly"],
                )
                creds = flow.run_local_server(port=0)
            with open(token_filename, "wb") as token:
                pickle.dump(creds, token)
    except Exception as e:
        logging.error(f"Error obtaining calendar credentials: {e}")
        return None
    return creds
