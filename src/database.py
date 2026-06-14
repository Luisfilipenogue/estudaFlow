"""Camada de persistência do EstudaFlow usando Supabase."""

import json
import os
import urllib.error
import urllib.request

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://cuidrohiptvgcvzljtjy.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_VK-v87zlbIOemszpXupv1g_MaICkmqi")


def _headers() -> dict:
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


def _request(method: str, path: str, body: dict | None = None) -> list | dict:
    url = f"{SUPABASE_URL}/rest/v1/{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=_headers(), method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else []
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Supabase error {e.code}: {e.read().decode()}") from e


# ─────────────────────────────────────── tasks ────────────────────────────────

def get_tasks() -> list[dict]:
    return _request("GET", "tasks?order=id.asc")


def add_task(
    title: str,
    subject: str = "",
    due: str | None = None,
    priority: str = "Média",
    notes: str = "",
) -> dict:
    if not title.strip():
        raise ValueError("O título da tarefa não pode ser vazio.")
    body = {
        "title": title,
        "subject": subject,
        "due": due,
        "priority": priority,
        "notes": notes,
        "done": False,
    }
    result = _request("POST", "tasks", body)
    return result[0] if isinstance(result, list) else result


def toggle_task(task_id: int, current_done: bool) -> dict:
    result = _request("PATCH", f"tasks?id=eq.{task_id}", {"done": not current_done})
    return result[0] if isinstance(result, list) else result


def delete_task(task_id: int) -> None:
    _request("DELETE", f"tasks?id=eq.{task_id}")


# ─────────────────────────────────────── subjects ─────────────────────────────

def get_subjects() -> list[dict]:
    return _request("GET", "subjects?order=id.asc")


def add_subject(name: str, teacher: str = "", color: str = "#6C63FF", notes: str = "") -> dict:
    if not name.strip():
        raise ValueError("O nome da disciplina não pode ser vazio.")
    body = {"name": name, "teacher": teacher, "color": color, "notes": notes}
    result = _request("POST", "subjects", body)
    return result[0] if isinstance(result, list) else result


def update_subject_notes(subject_id: int, notes: str) -> dict:
    """Atualiza as anotações de uma disciplina."""
    result = _request("PATCH", f"subjects?id=eq.{subject_id}", {"notes": notes})
    return result[0] if isinstance(result, list) else result


def delete_subject(subject_id: int) -> None:
    _request("DELETE", f"subjects?id=eq.{subject_id}")
