"""Testes de integração — EstudaFlow (Etapa Intermediária)."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import urllib.error

import pytest

from src.models import Task, Subject
from src.storage import Storage
from src.holidays import (
    fetch_holidays,
    format_holidays,
    get_upcoming_holidays,
    is_holiday,
)


# ══════════════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════════════

MOCK_HOLIDAYS_RAW = [
    {"date": "2025-01-01", "localName": "Confraternização Universal",
     "name": "New Year's Day", "countryCode": "BR"},
    {"date": "2025-04-21", "localName": "Tiradentes",
     "name": "Tiradentes' Day", "countryCode": "BR"},
    {"date": "2025-09-07", "localName": "Independência do Brasil",
     "name": "Independence Day", "countryCode": "BR"},
    {"date": "2025-11-02", "localName": "Finados",
     "name": "All Souls' Day", "countryCode": "BR"},
    {"date": "2025-12-25", "localName": "Natal",
     "name": "Christmas Day", "countryCode": "BR"},
]


def _mock_urlopen(raw: list[dict]):
    """Retorna um context-manager falso que simula urlopen."""
    mock_resp = MagicMock()
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__  = MagicMock(return_value=False)
    mock_resp.status = 200
    mock_resp.read.return_value = json.dumps(raw).encode("utf-8")
    return mock_resp


# ══════════════════════════════════════════════════════════════════════════════
# Testes da camada holidays.py
# ══════════════════════════════════════════════════════════════════════════════

class TestFetchHolidays:
    """Testa o consumo da API Nager.Date (com mock)."""

    def test_fetch_returns_list_on_success(self):
        """Simula resposta 200 da API e verifica retorno como lista."""
        with patch("urllib.request.urlopen", return_value=_mock_urlopen(MOCK_HOLIDAYS_RAW)):
            result = fetch_holidays(2025)
        assert isinstance(result, list)
        assert len(result) == 5

    def test_fetch_contains_expected_fields(self):
        """Os campos date, localName e name devem existir."""
        with patch("urllib.request.urlopen", return_value=_mock_urlopen(MOCK_HOLIDAYS_RAW)):
            result = fetch_holidays(2025)
        for h in result:
            assert "date" in h
            assert "localName" in h
            assert "name" in h

    def test_fetch_returns_empty_on_network_error(self):
        """Erro de rede deve retornar lista vazia, sem lançar exceção."""
        with patch(
            "urllib.request.urlopen",
            side_effect=urllib.error.URLError("network unreachable"),
        ):
            result = fetch_holidays(2025)
        assert result == []

    def test_fetch_returns_empty_on_invalid_json(self):
        """JSON inválido na resposta deve retornar lista vazia."""
        mock_resp = MagicMock()
        mock_resp.__enter__ = lambda s: s
        mock_resp.__exit__  = MagicMock(return_value=False)
        mock_resp.status = 200
        mock_resp.read.return_value = b"{broken json"
        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = fetch_holidays(2025)
        assert result == []

    def test_fetch_uses_current_year_by_default(self):
        """Sem argumento de ano, deve usar o ano corrente."""
        from datetime import date
        current_year = date.today().year
        captured_urls = []

        def fake_urlopen(url, timeout=None):
            captured_urls.append(url)
            return _mock_urlopen([])

        with patch("urllib.request.urlopen", side_effect=fake_urlopen):
            fetch_holidays()

        assert str(current_year) in captured_urls[0]


class TestFormatHolidays:
    """Testa a normalização dos dados da API."""

    def test_format_returns_sorted_by_date(self):
        raw = [
            {"date": "2025-12-25", "name": "Christmas", "localName": "Natal"},
            {"date": "2025-01-01", "name": "New Year", "localName": "Ano Novo"},
        ]
        result = format_holidays(raw)
        assert result[0]["date"] == "2025-01-01"
        assert result[1]["date"] == "2025-12-25"

    def test_format_keeps_required_keys_only(self):
        result = format_holidays(MOCK_HOLIDAYS_RAW)
        for h in result:
            assert set(h.keys()) == {"date", "name", "localName"}

    def test_format_empty_list(self):
        assert format_holidays([]) == []

    def test_format_handles_missing_fields(self):
        raw = [{"date": "2025-06-15"}]
        result = format_holidays(raw)
        assert result[0]["name"] == ""
        assert result[0]["localName"] == ""


class TestGetUpcomingHolidays:
    """Testa filtragem de próximos feriados."""

    def test_returns_at_most_limit(self):
        holidays = format_holidays(MOCK_HOLIDAYS_RAW)
        # Injeta datas futuras garantidas
        future = [
            {"date": "2099-01-01", "name": "A", "localName": "A"},
            {"date": "2099-02-01", "name": "B", "localName": "B"},
            {"date": "2099-03-01", "name": "C", "localName": "C"},
        ]
        result = get_upcoming_holidays(future, limit=2)
        assert len(result) == 2

    def test_excludes_past_dates(self):
        past = [
            {"date": "2000-01-01", "name": "Past", "localName": "Passado"},
        ]
        result = get_upcoming_holidays(past)
        assert result == []

    def test_empty_input(self):
        assert get_upcoming_holidays([]) == []


class TestIsHoliday:
    """Testa verificação se uma data é feriado."""

    def test_known_holiday(self):
        holidays = format_holidays(MOCK_HOLIDAYS_RAW)
        assert is_holiday("2025-12-25", holidays) is True

    def test_non_holiday(self):
        holidays = format_holidays(MOCK_HOLIDAYS_RAW)
        assert is_holiday("2025-06-10", holidays) is False

    def test_empty_list(self):
        assert is_holiday("2025-01-01", []) is False


# ══════════════════════════════════════════════════════════════════════════════
# Testes das rotas Flask
# ══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def flask_client(tmp_path):
    """Cria cliente de teste Flask com storage temporário."""
    import app as flask_app_module

    data_file = tmp_path / "data.json"
    st = Storage(data_file)
    flask_app_module.storage = st
    flask_app_module._holidays_cache = {}
    flask_app_module.app.config["TESTING"] = True

    with flask_app_module.app.test_client() as client:
        yield client


class TestFlaskRoutes:
    def test_index_returns_200(self, flask_client):
        with patch("src.holidays.fetch_holidays", return_value=MOCK_HOLIDAYS_RAW):
            resp = flask_client.get("/")
        assert resp.status_code == 200

    def test_tarefas_returns_200(self, flask_client):
        resp = flask_client.get("/tarefas")
        assert resp.status_code == 200

    def test_disciplinas_returns_200(self, flask_client):
        resp = flask_client.get("/disciplinas")
        assert resp.status_code == 200

    def test_feriados_returns_200(self, flask_client):
        with patch("src.holidays.fetch_holidays", return_value=MOCK_HOLIDAYS_RAW):
            resp = flask_client.get("/feriados")
        assert resp.status_code == 200

    def test_api_add_task(self, flask_client):
        resp = flask_client.post(
            "/api/tasks",
            json={"title": "Estudar Flask", "priority": "Alta"},
        )
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["ok"] is True
        assert data["task"]["title"] == "Estudar Flask"

    def test_api_add_task_empty_title(self, flask_client):
        resp = flask_client.post("/api/tasks", json={"title": ""})
        assert resp.status_code == 400
        assert resp.get_json()["ok"] is False

    def test_api_toggle_task(self, flask_client):
        flask_client.post("/api/tasks", json={"title": "Toggle"})
        resp = flask_client.post("/api/tasks/0/toggle")
        assert resp.status_code == 200
        assert resp.get_json()["done"] is True

    def test_api_delete_task(self, flask_client):
        flask_client.post("/api/tasks", json={"title": "Para deletar"})
        resp = flask_client.delete("/api/tasks/0")
        assert resp.status_code == 200
        assert resp.get_json()["ok"] is True

    def test_api_delete_task_invalid_index(self, flask_client):
        resp = flask_client.delete("/api/tasks/999")
        assert resp.status_code == 404

    def test_api_add_subject(self, flask_client):
        resp = flask_client.post("/api/subjects", json={"name": "Física"})
        assert resp.status_code == 201
        assert resp.get_json()["subject"]["name"] == "Física"

    def test_api_add_duplicate_subject(self, flask_client):
        flask_client.post("/api/subjects", json={"name": "Química"})
        resp = flask_client.post("/api/subjects", json={"name": "Química"})
        assert resp.status_code == 400

    def test_api_holidays_endpoint(self, flask_client):
        with patch("src.holidays.fetch_holidays", return_value=MOCK_HOLIDAYS_RAW):
            resp = flask_client.get("/api/holidays?year=2025")
        assert resp.status_code == 200
        data = resp.get_json()
        assert isinstance(data, list)
