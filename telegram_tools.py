import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def send_telegram_message(text):
    response = requests.get(
        TELEGRAM_URL, params={
            "chat_id": CHAT_ID,
            "text": text
        }
    )
    status_code = response.status_code
    if status_code != 200:
        return f"Fehler beim Senden der Nachricht an Telegram. Statuscode: {status_code}"