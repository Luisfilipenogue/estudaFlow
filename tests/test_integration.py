"""Testes de integração — EstudaFlow com Supabase."""

import json
from unittest.mock import patch, MagicMock
import urllib.error

import pytest

from src.holidays import (
    fetch_holidays, format_holidays,
    get_upcoming_holidays, is_holiday,
)

# ── Mock data ─────────────────────────────────────────────────────────────────

MOCK_HOLIDAYS_RAW = [
    {"date": "2025-01-01", "localName": "Ano Novo",       "name": "New Year's Day"},
    {"date": "2025-04-21", "localName": "Tiradentes",     "name": "Tiradentes' Day"},
    {"date": "2025-09-07", "localName": "Independência",  "name": "Independence Day"},
    {"date": "2025-12-25", "localName": "Natal",          "name": "Christmas Day"},
]

MOCK_TASKS = [
    {"id": 1, "title": "Estudar Flask", "subject": "TI", "due": "2025-12-01",
     "priority": "Alta", "notes": "", "done": False},
    {"id": 2, "title": "Revisar prova", "subject": "TI", "due": None,
     "priority": "Média", "notes": "", "done": True},
]

MOCK_SUBJECTS = [
    {"id": 1, "name": "TI", "teacher": "Prof. Ana", "color": "#6C63FF"},
]


def _mock_urlopen_holidays(raw):
    m = MagicMock()
    m.__enter__ = lambda s: s
    m.__exit__ = MagicMock(return_value=False)
    m.status = 200
    m.read.return_value = json.dumps(raw).encode()
    return m


# ── Holidays ──────────────────────────────────────────────────────────────────

class TestFetchHolidays:
    def test_fetch_returns_list_on_success(self):
        with patch("urllib.request.urlopen",
                   return_value=_mock_urlopen_holidays(MOCK_HOLIDAYS_RAW)):
            result = fetch_holidays(2025)
        assert isinstance(result, list)
        assert len(result) == 4

    def test_fetch_contains_expected_fields(self):
        with patch("urllib.request.urlopen",
                   return_value=_mock_urlopen_holidays(MOCK_HOLIDAYS_RAW)):
            result = fetch_holidays(2025)
        for h in result:
            assert "date" in h
            assert "localName" in h

    def test_fetch_returns_empty_on_network_error(self):
        with patch("urllib.request.urlopen",
                   side_effect=urllib.error.URLError("err")):
            result = fetch_holidays(2025)
        assert result == []

    def test_fetch_returns_empty_on_invalid_json(self):
        m = MagicMock()
        m.__enter__ = lambda s: s
        m.__exit__ = MagicMock(return_value=False)
        m.status = 200
        m.read.return_value = b"{broken"
        with patch("urllib.request.urlopen", return_value=m):
            result = fetch_holidays(2025)
        assert result == []

    def test_fetch_uses_current_year_by_default(self):
        from datetime import date
        captured = []
        def fake(url, timeout=None):
            captured.append(url)
            return _mock_urlopen_holidays([])
        with patch("urllib.request.urlopen", side_effect=fake):
            fetch_holidays()
        assert str(date.today().year) in captured[0]


class TestFormatHolidays:
    def test_sorted_by_date(self):
        raw = [
            {"date": "2025-12-25", "name": "C", "localName": "Natal"},
            {"date": "2025-01-01", "name": "A", "localName": "Ano Novo"},
        ]
        result = format_holidays(raw)
        assert result[0]["date"] == "2025-01-01"

    def test_empty_input(self):
        assert format_holidays([]) == []


class TestGetUpcomingHolidays:
    def test_returns_at_most_limit(self):
        future = [
            {"date": "2099-01-01", "name": "A", "localName": "A"},
            {"date": "2099-02-01", "name": "B", "localName": "B"},
            {"date": "2099-03-01", "name": "C", "localName": "C"},
        ]
        assert len(get_upcoming_holidays(future, limit=2)) == 2

    def test_excludes_past(self):
        past = [{"date": "2000-01-01", "name": "P", "localName": "P"}]
        assert get_upcoming_holidays(past) == []


class TestIsHoliday:
    def test_known_holiday(self):
        h = format_holidays(MOCK_HOLIDAYS_RAW)
        assert is_holiday("2025-12-25", h) is True

    def test_non_holiday(self):
        h = format_holidays(MOCK_HOLIDAYS_RAW)
        assert is_holiday("2025-06-10", h) is False


# ── Flask routes ──────────────────────────────────────────────────────────────

@pytest.fixture
def client():
    import app as flask_app
    flask_app.app.config["TESTING"] = True
    flask_app._holidays_cache = {}
    with flask_app.app.test_client() as c:
        yield c


class TestFlaskRoutes:
    def test_index_returns_200(self, client):
        with patch("app.get_tasks", return_value=MOCK_TASKS), \
             patch("app.get_subjects", return_value=MOCK_SUBJECTS), \
             patch("src.holidays.fetch_holidays", return_value=MOCK_HOLIDAYS_RAW):
            resp = client.get("/")
        assert resp.status_code == 200

    def test_tarefas_returns_200(self, client):
        with patch("app.get_tasks", return_value=MOCK_TASKS), \
             patch("app.get_subjects", return_value=MOCK_SUBJECTS):
            resp = client.get("/tarefas")
        assert resp.status_code == 200

    def test_disciplinas_returns_200(self, client):
        with patch("app.get_subjects", return_value=MOCK_SUBJECTS), \
             patch("app.get_tasks", return_value=MOCK_TASKS):
            resp = client.get("/disciplinas")
        assert resp.status_code == 200

    def test_feriados_returns_200(self, client):
        with patch("src.holidays.fetch_holidays", return_value=MOCK_HOLIDAYS_RAW):
            resp = client.get("/feriados")
        assert resp.status_code == 200

    def test_api_add_task_success(self, client):
        new_task = {"id": 3, "title": "Nova", "subject": "", "due": None,
                    "priority": "Média", "notes": "", "done": False}
        with patch("app.add_task", return_value=new_task):
            resp = client.post("/api/tasks", json={"title": "Nova"})
        assert resp.status_code == 201
        assert resp.get_json()["ok"] is True

    def test_api_add_task_empty_title(self, client):
        with patch("app.add_task", side_effect=ValueError("título vazio")):
            resp = client.post("/api/tasks", json={"title": ""})
        assert resp.status_code == 400

    def test_api_toggle_task(self, client):
        updated = {**MOCK_TASKS[0], "done": True}
        with patch("app.get_tasks", return_value=MOCK_TASKS), \
             patch("app.toggle_task", return_value=updated):
            resp = client.post("/api/tasks/1/toggle")
        assert resp.status_code == 200
        assert resp.get_json()["done"] is True

    def test_api_delete_task(self, client):
        with patch("app.delete_task", return_value=None):
            resp = client.delete("/api/tasks/1")
        assert resp.status_code == 200
        assert resp.get_json()["ok"] is True

    def test_api_add_subject_success(self, client):
        new_subj = {"id": 2, "name": "Física", "teacher": "", "color": "#6C63FF"}
        with patch("app.add_subject", return_value=new_subj):
            resp = client.post("/api/subjects", json={"name": "Física"})
        assert resp.status_code == 201

    def test_api_holidays_endpoint(self, client):
        with patch("src.holidays.fetch_holidays", return_value=MOCK_HOLIDAYS_RAW):
            resp = client.get("/api/holidays?year=2025")
        assert resp.status_code == 200
        assert isinstance(resp.get_json(), list)
