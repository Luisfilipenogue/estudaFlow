"""Camada de persistência do EstudaFlow (JSON)."""

import json
from pathlib import Path

from src.models import Task, Subject


class Storage:
    """Gerencia leitura e escrita dos dados em JSON."""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.tasks: list[Task] = []
        self.subjects: list[Subject] = []

    # ------------------------------------------------------------------ public
    def load(self) -> None:
        """Carrega dados do arquivo JSON. Ignora se não existir."""
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
        """Persiste dados no arquivo JSON."""
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "tasks": [t.to_dict() for t in self.tasks],
            "subjects": [s.to_dict() for s in self.subjects],
        }
        self.filepath.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # ------------------------------------------------------------------ tasks
    def add_task(self, task: Task) -> None:
        """Adiciona uma nova tarefa."""
        if not task.title.strip():
            raise ValueError("O título da tarefa não pode ser vazio.")
        self.tasks.append(task)

    def remove_task(self, index: int) -> None:
        """Remove tarefa pelo índice."""
        if index < 0 or index >= len(self.tasks):
            raise IndexError(f"Índice {index} fora do intervalo.")
        self.tasks.pop(index)

    def toggle_task(self, index: int) -> None:
        """Alterna o status de conclusão de uma tarefa."""
        if index < 0 or index >= len(self.tasks):
            raise IndexError(f"Índice {index} fora do intervalo.")
        self.tasks[index].done = not self.tasks[index].done

    def get_pending_tasks(self) -> list[Task]:
        """Retorna tarefas ainda não concluídas."""
        return [t for t in self.tasks if not t.done]

    def get_tasks_by_subject(self, subject: str) -> list[Task]:
        """Filtra tarefas por disciplina."""
        return [t for t in self.tasks if t.subject == subject]

    # ------------------------------------------------------------------ subjects
    def add_subject(self, subject: Subject) -> None:
        """Adiciona uma nova disciplina."""
        if not subject.name.strip():
            raise ValueError("O nome da disciplina não pode ser vazio.")
        names = [s.name for s in self.subjects]
        if subject.name in names:
            raise ValueError(f"Disciplina '{subject.name}' já existe.")
        self.subjects.append(subject)

    def remove_subject(self, index: int) -> None:
        """Remove disciplina pelo índice."""
        if index < 0 or index >= len(self.subjects):
            raise IndexError(f"Índice {index} fora do intervalo.")
        self.subjects.pop(index)
