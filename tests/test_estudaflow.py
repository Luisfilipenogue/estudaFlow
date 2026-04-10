"""Testes automatizados do EstudaFlow."""

import json
import tempfile
from pathlib import Path

import pytest

from src.models import Task, Subject
from src.storage import Storage


# ───────────────────────────── helpers ──────────────────────────────────────

def make_storage() -> Storage:
    """Retorna um Storage em diretório temporário."""
    tmp = Path(tempfile.mkdtemp()) / "data.json"
    return Storage(tmp)


# ═══════════════════════════ Task model ══════════════════════════════════════

class TestTaskModel:
    def test_default_values(self):
        t = Task(title="Estudar álgebra")
        assert t.title == "Estudar álgebra"
        assert t.done is False
        assert t.priority == "Média"
        assert t.subject == ""

    def test_to_dict_round_trip(self):
        t = Task(title="Revisar capítulo 3", subject="Física",
                 priority="Alta", due="2025-12-01", notes="ver págs 40-60")
        d = t.to_dict()
        t2 = Task.from_dict(d)
        assert t2.title == t.title
        assert t2.subject == t.subject
        assert t2.due == t.due
        assert t2.priority == t.priority
        assert t2.notes == t.notes
        assert t2.done == t.done

    def test_from_dict_missing_fields(self):
        """Campos ausentes devem usar valores padrão."""
        t = Task.from_dict({"title": "Só título"})
        assert t.subject == ""
        assert t.due is None
        assert t.done is False


# ═══════════════════════════ Subject model ═══════════════════════════════════

class TestSubjectModel:
    def test_default_color(self):
        s = Subject(name="Matemática")
        assert s.color == "#6C63FF"

    def test_to_dict_round_trip(self):
        s = Subject(name="História", teacher="Prof. Ana", color="#FF6363")
        d = s.to_dict()
        s2 = Subject.from_dict(d)
        assert s2.name == s.name
        assert s2.teacher == s.teacher
        assert s2.color == s.color


# ═══════════════════════════ Storage — tasks ═════════════════════════════════

class TestStorageTasks:
    def test_add_and_retrieve_task(self):
        st = make_storage()
        st.add_task(Task(title="Tarefa 1"))
        assert len(st.tasks) == 1
        assert st.tasks[0].title == "Tarefa 1"

    def test_add_task_empty_title_raises(self):
        st = make_storage()
        with pytest.raises(ValueError, match="vazio"):
            st.add_task(Task(title="   "))

    def test_remove_task(self):
        st = make_storage()
        st.add_task(Task(title="A"))
        st.add_task(Task(title="B"))
        st.remove_task(0)
        assert len(st.tasks) == 1
        assert st.tasks[0].title == "B"

    def test_remove_task_invalid_index(self):
        st = make_storage()
        with pytest.raises(IndexError):
            st.remove_task(99)

    def test_toggle_task(self):
        st = make_storage()
        st.add_task(Task(title="Toggle me"))
        assert st.tasks[0].done is False
        st.toggle_task(0)
        assert st.tasks[0].done is True
        st.toggle_task(0)
        assert st.tasks[0].done is False

    def test_toggle_task_invalid_index(self):
        st = make_storage()
        with pytest.raises(IndexError):
            st.toggle_task(0)

    def test_get_pending_tasks(self):
        st = make_storage()
        st.add_task(Task(title="Pendente"))
        st.add_task(Task(title="Feita", done=True))
        pending = st.get_pending_tasks()
        assert len(pending) == 1
        assert pending[0].title == "Pendente"

    def test_get_tasks_by_subject(self):
        st = make_storage()
        st.add_task(Task(title="T1", subject="Física"))
        st.add_task(Task(title="T2", subject="Química"))
        st.add_task(Task(title="T3", subject="Física"))
        fisica = st.get_tasks_by_subject("Física")
        assert len(fisica) == 2

    def test_get_tasks_by_subject_no_match(self):
        st = make_storage()
        st.add_task(Task(title="T1", subject="Física"))
        result = st.get_tasks_by_subject("Matemática")
        assert result == []


# ═══════════════════════════ Storage — subjects ══════════════════════════════

class TestStorageSubjects:
    def test_add_subject(self):
        st = make_storage()
        st.add_subject(Subject(name="Biologia"))
        assert len(st.subjects) == 1

    def test_add_subject_empty_name_raises(self):
        st = make_storage()
        with pytest.raises(ValueError):
            st.add_subject(Subject(name=""))

    def test_add_duplicate_subject_raises(self):
        st = make_storage()
        st.add_subject(Subject(name="Química"))
        with pytest.raises(ValueError, match="já existe"):
            st.add_subject(Subject(name="Química"))

    def test_remove_subject(self):
        st = make_storage()
        st.add_subject(Subject(name="Arte"))
        st.remove_subject(0)
        assert st.subjects == []

    def test_remove_subject_invalid_index(self):
        st = make_storage()
        with pytest.raises(IndexError):
            st.remove_subject(5)


# ═══════════════════════════ Storage — persistence ═══════════════════════════

class TestStoragePersistence:
    def test_save_and_load(self):
        tmp = Path(tempfile.mkdtemp()) / "data.json"
        st = Storage(tmp)
        st.add_task(Task(title="Persistida", subject="Geo", priority="Alta"))
        st.add_subject(Subject(name="Geo", teacher="Prof. X"))
        st.save()

        st2 = Storage(tmp)
        st2.load()
        assert len(st2.tasks) == 1
        assert st2.tasks[0].title == "Persistida"
        assert len(st2.subjects) == 1
        assert st2.subjects[0].name == "Geo"

    def test_load_nonexistent_file_is_ok(self):
        tmp = Path(tempfile.mkdtemp()) / "missing.json"
        st = Storage(tmp)
        st.load()
        assert st.tasks == []
        assert st.subjects == []

    def test_load_corrupted_json(self):
        tmp = Path(tempfile.mkdtemp()) / "bad.json"
        tmp.write_text("{invalid json", encoding="utf-8")
        st = Storage(tmp)
        st.load()
        assert st.tasks == []

    def test_save_creates_parent_dirs(self):
        tmp = Path(tempfile.mkdtemp()) / "deep" / "nested" / "data.json"
        st = Storage(tmp)
        st.save()
        assert tmp.exists()
