"""EstudaFlow — aplicação Flask com Supabase."""

from datetime import date

from flask import Flask, jsonify, render_template, request

from src.database import (
    add_subject,
    add_task,
    delete_subject,
    delete_task,
    get_subjects,
    get_tasks,
    toggle_task,
    update_subject_notes,
)
from src.holidays import fetch_holidays, format_holidays, get_upcoming_holidays, is_holiday

app = Flask(__name__)

_holidays_cache: dict[int, list[dict]] = {}


def _get_holidays(year: int | None = None) -> list[dict]:
    y = year or date.today().year
    if y not in _holidays_cache:
        raw = fetch_holidays(y)
        _holidays_cache[y] = format_holidays(raw)
    return _holidays_cache[y]


# ─────────────────────────────────────── páginas ──────────────────────────────


@app.route("/")
def index():
    try:
        tasks = get_tasks()
        subjects = get_subjects()
    except Exception:
        tasks, subjects = [], []

    holidays = _get_holidays()
    upcoming = get_upcoming_holidays(holidays, limit=5)
    total = len(tasks)
    done = sum(1 for t in tasks if t.get("done"))
    pending = total - done
    overdue = sum(
        1
        for t in tasks
        if not t.get("done") and t.get("due") and t["due"] < date.today().isoformat()
    )
    return render_template(
        "index.html",
        tasks=tasks,
        subjects=subjects,
        upcoming_holidays=upcoming,
        total=total,
        done=done,
        pending=pending,
        overdue=overdue,
        today=date.today().isoformat(),
    )


@app.route("/tarefas")
def tarefas():
    try:
        tasks = get_tasks()
        subjects = get_subjects()
    except Exception:
        tasks, subjects = [], []

    holidays = _get_holidays()
    tasks_with_flag = [
        {"task": t, "is_holiday": is_holiday(t.get("due", ""), holidays)} for t in tasks
    ]
    return render_template("tarefas.html", tasks_with_flag=tasks_with_flag, subjects=subjects)


@app.route("/disciplinas")
def disciplinas():
    try:
        subjects = get_subjects()
        tasks = get_tasks()
    except Exception:
        subjects, tasks = [], []

    subjects_with_count = [
        {"subject": s, "count": sum(1 for t in tasks if t.get("subject") == s["name"])}
        for s in subjects
    ]
    return render_template("disciplinas.html", subjects_with_count=subjects_with_count)


@app.route("/feriados")
def feriados():
    year = request.args.get("year", date.today().year, type=int)
    holidays = _get_holidays(year)
    return render_template("feriados.html", holidays=holidays, year=year)


# ─────────────────────────────────────── API JSON ─────────────────────────────


@app.route("/api/tasks", methods=["GET"])
def api_get_tasks():
    return jsonify(get_tasks())


@app.route("/api/tasks", methods=["POST"])
def api_add_task():
    data = request.get_json(force=True)
    try:
        task = add_task(
            title=data.get("title", ""),
            subject=data.get("subject", ""),
            due=data.get("due") or None,
            priority=data.get("priority", "Média"),
            notes=data.get("notes", ""),
        )
        return jsonify({"ok": True, "task": task}), 201
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/tasks/<int:task_id>/toggle", methods=["POST"])
def api_toggle_task(task_id: int):
    try:
        tasks = get_tasks()
        task = next((t for t in tasks if t["id"] == task_id), None)
        if not task:
            return jsonify({"ok": False, "error": "Tarefa não encontrada."}), 404
        updated = toggle_task(task_id, task["done"])
        return jsonify({"ok": True, "done": updated.get("done")})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def api_delete_task(task_id: int):
    try:
        delete_task(task_id)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/subjects", methods=["GET"])
def api_get_subjects():
    return jsonify(get_subjects())


@app.route("/api/subjects", methods=["POST"])
def api_add_subject():
    data = request.get_json(force=True)
    try:
        subj = add_subject(
            name=data.get("name", ""),
            teacher=data.get("teacher", ""),
            color=data.get("color", "#6C63FF"),
            notes=data.get("notes", ""),
        )
        return jsonify({"ok": True, "subject": subj}), 201
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/subjects/<int:subject_id>", methods=["DELETE"])
def api_delete_subject(subject_id: int):
    try:
        delete_subject(subject_id)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/subjects/<int:subject_id>/notes", methods=["PATCH"])
def api_update_subject_notes(subject_id: int):
    """Atualiza as anotações de uma disciplina."""
    data = request.get_json(force=True)
    try:
        updated = update_subject_notes(subject_id, data.get("notes", ""))
        return jsonify({"ok": True, "subject": updated})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/holidays")
def api_holidays():
    year = request.args.get("year", date.today().year, type=int)
    return jsonify(_get_holidays(year))


if __name__ == "__main__":
    app.run(debug=True)
