"""Modelos de dados do EstudaFlow."""

from dataclasses import dataclass, field


@dataclass
class Task:
    """Representa uma tarefa de estudo."""

    title: str
    subject: str = ""
    due: str | None = None  # ISO date string YYYY-MM-DD
    priority: str = "Média"
    notes: str = ""
    done: bool = False

    def to_dict(self) -> dict:
        """Serializa a tarefa para dicionário."""
        return {
            "title": self.title,
            "subject": self.subject,
            "due": self.due,
            "priority": self.priority,
            "notes": self.notes,
            "done": self.done,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Desserializa uma tarefa a partir de dicionário."""
        return cls(
            title=data.get("title", ""),
            subject=data.get("subject", ""),
            due=data.get("due"),
            priority=data.get("priority", "Média"),
            notes=data.get("notes", ""),
            done=data.get("done", False),
        )


@dataclass
class Subject:
    """Representa uma disciplina de estudo."""

    name: str
    teacher: str = ""
    color: str = "#6C63FF"

    def to_dict(self) -> dict:
        """Serializa a disciplina para dicionário."""
        return {
            "name": self.name,
            "teacher": self.teacher,
            "color": self.color,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Subject":
        """Desserializa uma disciplina a partir de dicionário."""
        return cls(
            name=data.get("name", ""),
            teacher=data.get("teacher", ""),
            color=data.get("color", "#6C63FF"),
        )
