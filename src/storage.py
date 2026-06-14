"""Camada de persistência do EstudaFlow (JSON)."""

import json
from pathlib import Path

from src.models import Subject, Task


class Storage:
    """Gerencia leitura e escrita dos dados em JSON."""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.tasks: list[Task] = []
        self.subjects: list[Subject] = []

    def load(self) -> None:
        if not self.filepath.exists():
            return
        try:
            raw = json.loads(self.filepath.read_text(encoding="utf-8"))
            self.tasks = [Task.from_dict(t) for t in raw.get("tasks", [])]
            self.subjects = [Subject.from_dict(s) for s in raw.get("subjects", [])]
        except (json.JSONDecodeError, KeyError):
            self.tasks = []
            self.subjects = []

    def save(self) -> None:
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "tasks": [t.to_dict() for t in self.tasks],
            "subjects": [s.to_dict() for s in self.subjects],
        }
        self.filepath.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def add_task(self, task: Task) -> None:
        if not task.title.strip():
            raise ValueError("O título da tarefa não pode ser vazio.")
        self.tasks.append(task)

    def remove_task(self, index: int) -> None:
        if index < 0 or index >= len(self.tasks):
            raise IndexError(f"Índice {index} fora do intervalo.")
        self.tasks.pop(index)

    def toggle_task(self, index: int) -> None:
        if index < 0 or index >= len(self.tasks):
            raise IndexError(f"Índice {index} fora do intervalo.")
        self.tasks[index].done = not self.tasks[index].done

    def get_pending_tasks(self) -> list[Task]:
        return [t for t in self.tasks if not t.done]

    def get_tasks_by_subject(self, subject: str) -> list[Task]:
        return [t for t in self.tasks if t.subject == subject]

    def add_subject(self, subject: Subject) -> None:
        if not subject.name.strip():
            raise ValueError("O nome da disciplina não pode ser vazio.")
        names = [s.name for s in self.subjects]
        if subject.name in names:
            raise ValueError(f"Disciplina '{subject.name}' já existe.")
        self.subjects.append(subject)

    def remove_subject(self, index: int) -> None:
        if index < 0 or index >= len(self.subjects):
            raise IndexError(f"Índice {index} fora do intervalo.")
        self.subjects.pop(index)
