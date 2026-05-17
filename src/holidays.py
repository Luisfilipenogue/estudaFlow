"""Integração com a API Nager.Date — feriados brasileiros."""

import urllib.request
import urllib.error
import json
from datetime import date


NAGER_BASE_URL = "https://date.nager.at/api/v3"
COUNTRY_CODE = "BR"


def fetch_holidays(year: int | None = None) -> list[dict]:
    """
    Busca feriados nacionais do Brasil via API Nager.Date.

    Args:
        year: Ano desejado. Usa o ano corrente se omitido.

    Returns:
        Lista de dicionários com os feriados ou lista vazia em caso de falha.

    Raises:
        RuntimeError: se a requisição HTTP falhar com status inesperado.
    """
    if year is None:
        year = date.today().year

    url = f"{NAGER_BASE_URL}/PublicHolidays/{year}/{COUNTRY_CODE}"

    try:
        with urllib.request.urlopen(url, timeout=8) as response:
            if response.status != 200:
                raise RuntimeError(
                    f"API retornou status {response.status} para {url}"
                )
            raw = response.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.URLError as exc:
        # Falha de rede — retorna lista vazia para não quebrar a UI
        return []
    except json.JSONDecodeError:
        return []


def format_holidays(holidays: list[dict]) -> list[dict]:
    """
    Normaliza a lista de feriados retornada pela API.

    Retorna uma lista de dicts com as chaves:
        date (str YYYY-MM-DD), name (str), localName (str)
    """
    result = []
    for h in holidays:
        result.append(
            {
                "date": h.get("date", ""),
                "name": h.get("name", ""),
                "localName": h.get("localName", ""),
            }
        )
    return sorted(result, key=lambda x: x["date"])


def get_upcoming_holidays(holidays: list[dict], limit: int = 5) -> list[dict]:
    """Filtra os próximos feriados a partir de hoje."""
    today = date.today().isoformat()
    upcoming = [h for h in holidays if h.get("date", "") >= today]
    return upcoming[:limit]


def is_holiday(check_date: str, holidays: list[dict]) -> bool:
    """Verifica se uma data (YYYY-MM-DD) é feriado nacional."""
    return any(h.get("date") == check_date for h in holidays)
