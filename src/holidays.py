"""Integração com a API Nager.Date — feriados brasileiros."""

import urllib.request
import urllib.error
import json
from datetime import date

NAGER_BASE_URL = "https://date.nager.at/api/v3"
COUNTRY_CODE = "BR"


def fetch_holidays(year: int | None = None) -> list[dict]:
    if year is None:
        year = date.today().year
    url = f"{NAGER_BASE_URL}/PublicHolidays/{year}/{COUNTRY_CODE}"
    try:
        with urllib.request.urlopen(url, timeout=8) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw)
    except (urllib.error.URLError, json.JSONDecodeError):
        return []


def format_holidays(holidays: list[dict]) -> list[dict]:
    result = [
        {"date": h.get("date", ""), "name": h.get("name", ""),
         "localName": h.get("localName", "")}
        for h in holidays
    ]
    return sorted(result, key=lambda x: x["date"])


def get_upcoming_holidays(holidays: list[dict], limit: int = 5) -> list[dict]:
    today = date.today().isoformat()
    return [h for h in holidays if h.get("date", "") >= today][:limit]


def is_holiday(check_date: str, holidays: list[dict]) -> bool:
    return any(h.get("date") == check_date for h in holidays)
