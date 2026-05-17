"""EstudaFlow — aplicação Flask."""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from pathlib import Path
from datetime import date

from src.models import Task, Subject
from src.storage import Storage
from src.holidays import fetch_holidays, format_holidays, get_upcoming_holidays, is_holiday

DATA_FILE = Path("data.json")

app = Flask(__name__)
storage = Storage(DATA_FILE)
storage.load()

# Cache de feriados em memória (evita chamadas repetidas)
_holidays_cache: dict[int, list[dict]] = {}


def _get_holidays(year: int | None = None) -> list[dict]:
    """Retorna feriados formatados, usando cache."""
    y = year or date.today().year
    if y not in _holidays_cache:
        raw = fetch_holidays(y)
        _holidays_cache[y] = format_holidays(raw)
    return _holidays_cache[y]


# ─────────────────────────────────────────────── páginas ──────────────────────

@app.route("/")
def index():
    holidays = _get_holidays()
    upcoming = get_upcoming_holidays(holidays, limit=5)
    tasks = storage.tasks
    total = len(tasks)
    done = sum(1 for t in tasks if t.done)
    pending = total - done
    overdue = sum(
        1 for t in tasks
        if not t.done and t.due and t.due < date.today().isoformat()
    )
    return render_template(
        "index.html",
        tasks=tasks,
        subjects=storage.subjects,
        upcoming_holidays=upcoming,
        total=total,
        done=done,
        pending=pending,
        overdue=overdue,
        today=date.today().isoformat(),
    )


@app.route("/tarefas")
def tarefas():
    holidays = _get_holidays()
    tasks_with_flag = []
    for t in storage.tasks:
        flag = is_holiday(t.due, holidays) if t.due else False
        tasks_with_flag.append({"task": t, "is_holiday": flag})
    return render_template(
        "tarefas.html",
        tasks_with_flag=tasks_with_flag,
        subjects=storage.subjects,
    )


@app.route("/disciplinas")
def disciplinas():
    subjects_with_count = []
    for s in storage.subjects:
        count = sum(1 for t in storage.tasks if t.subject == s.name)
        subjects_with_count.append({"subject": s, "count": count})
    return render_template("disciplinas.html", subjects_with_count=subjects_with_count)


@app.route("/feriados")
def feriados():
    year = request.args.get("year", date.today().year, type=int)
    holidays = _get_holidays(year)
    return render_template("feriados.html", holidays=holidays, year=year)


# ─────────────────────────────────────────────── API JSON ─────────────────────

@app.route("/api/tasks", methods=["GET"])
def api_get_tasks():
    return jsonify([t.to_dict() for t in storage.tasks])


@app.route("/api/tasks", methods=["POST"])
def api_add_task():
    data = request.get_json(force=True)
    try:
        task = Task(
            title=data.get("title", ""),
            subject=data.get("subject", ""),
            due=data.get("due") or None,
            priority=data.get("priority", "Média"),
            notes=data.get("notes", ""),
        )
        storage.add_task(task)
        storage.save()
        return jsonify({"ok": True, "task": task.to_dict()}), 201
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400


@app.route("/api/tasks/<int:idx>/toggle", methods=["POST"])
def api_toggle_task(idx: int):
    try:
        storage.toggle_task(idx)
        storage.save()
        return jsonify({"ok": True, "done": storage.tasks[idx].done})
    except IndexError as e:
        return jsonify({"ok": False, "error": str(e)}), 404


@app.route("/api/tasks/<int:idx>", methods=["DELETE"])
def api_delete_task(idx: int):
    try:
        storage.remove_task(idx)
        storage.save()
        return jsonify({"ok": True})
    except IndexError as e:
        return jsonify({"ok": False, "error": str(e)}), 404


@app.route("/api/subjects", methods=["GET"])
def api_get_subjects():
    return jsonify([s.to_dict() for s in storage.subjects])


@app.route("/api/subjects", methods=["POST"])
def api_add_subject():
    data = request.get_json(force=True)
    try:
        subj = Subject(
            name=data.get("name", ""),
            teacher=data.get("teacher", ""),
            color=data.get("color", "#6C63FF"),
        )
        storage.add_subject(subj)
        storage.save()
        return jsonify({"ok": True, "subject": subj.to_dict()}), 201
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400


@app.route("/api/subjects/<int:idx>", methods=["DELETE"])
def api_delete_subject(idx: int):
    try:
        storage.remove_subject(idx)
        storage.save()
        return jsonify({"ok": True})
    except IndexError as e:
        return jsonify({"ok": False, "error": str(e)}), 404


@app.route("/api/holidays")
def api_holidays():
    year = request.args.get("year", date.today().year, type=int)
    holidays = _get_holidays(year)
    return jsonify(holidays)


if __name__ == "__main__":
    app.run(debug=True)
