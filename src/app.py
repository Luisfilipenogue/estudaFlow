"""EstudaFlow - Organizador de Estudos para Estudantes."""

import json
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, date
from pathlib import Path

from src.storage import Storage
from src.models import Task, Subject


DATA_FILE = Path.home() / ".estudaflow" / "data.json"


class EstudaFlowApp:
    """Aplicação principal do EstudaFlow."""

    def __init__(self, root: tk.Tk, storage: Storage | None = None):
        self.root = root
        self.storage = storage or Storage(DATA_FILE)
        self.root.title("EstudaFlow — Organizador de Estudos")
        self.root.geometry("960x680")
        self.root.configure(bg="#0F1117")
        self.root.resizable(True, True)
        self._setup_styles()
        self._build_ui()
        self._load_data()

    # ------------------------------------------------------------------ styles
    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Card.TFrame",
            background="#1A1D2E",
            relief="flat",
        )
        style.configure(
            "Header.TLabel",
            background="#0F1117",
            foreground="#E2E8F0",
            font=("Georgia", 22, "bold"),
        )
        style.configure(
            "Sub.TLabel",
            background="#0F1117",
            foreground="#94A3B8",
            font=("Georgia", 11),
        )
        style.configure(
            "Card.TLabel",
            background="#1A1D2E",
            foreground="#E2E8F0",
            font=("Courier New", 11),
        )
        style.configure(
            "Accent.TButton",
            background="#6C63FF",
            foreground="#FFFFFF",
            font=("Courier New", 10, "bold"),
            borderwidth=0,
            focusthickness=0,
            relief="flat",
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#8B85FF"), ("pressed", "#5A52D5")],
        )
        style.configure(
            "Danger.TButton",
            background="#EF4444",
            foreground="#FFFFFF",
            font=("Courier New", 10, "bold"),
            borderwidth=0,
            focusthickness=0,
            relief="flat",
        )
        style.map(
            "Danger.TButton",
            background=[("active", "#F87171")],
        )
        style.configure(
            "Treeview",
            background="#1A1D2E",
            foreground="#E2E8F0",
            fieldbackground="#1A1D2E",
            font=("Courier New", 10),
            rowheight=32,
        )
        style.configure(
            "Treeview.Heading",
            background="#252840",
            foreground="#94A3B8",
            font=("Courier New", 10, "bold"),
            relief="flat",
        )
        style.map(
            "Treeview",
            background=[("selected", "#6C63FF")],
            foreground=[("selected", "#FFFFFF")],
        )

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        # ── Header
        header = tk.Frame(self.root, bg="#0F1117")
        header.pack(fill="x", padx=32, pady=(28, 0))

        tk.Label(
            header,
            text="EstudaFlow",
            bg="#0F1117",
            fg="#E2E8F0",
            font=("Georgia", 26, "bold"),
        ).pack(side="left")
        tk.Label(
            header,
            text="  ✦  organizador de estudos",
            bg="#0F1117",
            fg="#6C63FF",
            font=("Georgia", 13, "italic"),
        ).pack(side="left", pady=(6, 0))

        # ── Notebook / abas
        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True, padx=32, pady=20)

        self.tab_tasks = tk.Frame(nb, bg="#0F1117")
        self.tab_subjects = tk.Frame(nb, bg="#0F1117")
        self.tab_summary = tk.Frame(nb, bg="#0F1117")

        nb.add(self.tab_tasks, text="  Tarefas  ")
        nb.add(self.tab_subjects, text="  Disciplinas  ")
        nb.add(self.tab_summary, text="  Resumo  ")

        self._build_tasks_tab()
        self._build_subjects_tab()
        self._build_summary_tab()

    # ------------------------------------------------------------------ TASKS
    def _build_tasks_tab(self):
        parent = self.tab_tasks

        # ── form
        form = tk.Frame(parent, bg="#1A1D2E", pady=16, padx=20)
        form.pack(fill="x", pady=(0, 12))

        tk.Label(form, text="Nova Tarefa", bg="#1A1D2E", fg="#6C63FF",
                 font=("Georgia", 13, "bold")).grid(row=0, column=0, columnspan=6,
                                                    sticky="w", pady=(0, 10))

        lbl = lambda t: tk.Label(form, text=t, bg="#1A1D2E", fg="#94A3B8",
                                 font=("Courier New", 9))
        ent = lambda w=22: tk.Entry(form, width=w, bg="#252840", fg="#E2E8F0",
                                    insertbackground="#E2E8F0",
                                    font=("Courier New", 10), relief="flat",
                                    bd=4)

        lbl("Título *").grid(row=1, column=0, sticky="w")
        self.task_title = ent(26)
        self.task_title.grid(row=1, column=1, padx=(4, 12))

        lbl("Disciplina").grid(row=1, column=2, sticky="w")
        self.task_subject_var = tk.StringVar()
        self.task_subject_combo = ttk.Combobox(
            form, textvariable=self.task_subject_var, width=18,
            font=("Courier New", 10), state="readonly"
        )
        self.task_subject_combo.grid(row=1, column=3, padx=(4, 12))

        lbl("Prazo (DD/MM/AAAA)").grid(row=1, column=4, sticky="w")
        self.task_due = ent(14)
        self.task_due.grid(row=1, column=5, padx=(4, 12))

        lbl("Prioridade").grid(row=2, column=0, sticky="w", pady=(8, 0))
        self.task_priority = ttk.Combobox(
            form, values=["Alta", "Média", "Baixa"], width=10,
            font=("Courier New", 10), state="readonly"
        )
        self.task_priority.set("Média")
        self.task_priority.grid(row=2, column=1, sticky="w", padx=(4, 12),
                                pady=(8, 0))

        lbl("Notas").grid(row=2, column=2, sticky="w", pady=(8, 0))
        self.task_notes = ent(34)
        self.task_notes.grid(row=2, column=3, columnspan=2, sticky="w",
                             padx=(4, 12), pady=(8, 0))

        ttk.Button(form, text="+ Adicionar", style="Accent.TButton",
                   command=self._add_task).grid(row=2, column=5, padx=(4, 0),
                                                pady=(8, 0))

        # ── list
        cols = ("title", "subject", "due", "priority", "done")
        self.task_tree = ttk.Treeview(parent, columns=cols, show="headings",
                                      height=14)
        for col, head, w in [
            ("title", "Título", 220),
            ("subject", "Disciplina", 140),
            ("due", "Prazo", 100),
            ("priority", "Prioridade", 90),
            ("done", "Status", 90),
        ]:
            self.task_tree.heading(col, text=head)
            self.task_tree.column(col, width=w, anchor="w")

        sb = ttk.Scrollbar(parent, orient="vertical",
                           command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=sb.set)
        self.task_tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="left", fill="y")

        btn_row = tk.Frame(self.tab_tasks, bg="#0F1117")
        btn_row.pack(fill="x", pady=8)
        ttk.Button(btn_row, text="✔ Marcar concluída",
                   style="Accent.TButton",
                   command=self._toggle_task).pack(side="left", padx=(0, 8))
        ttk.Button(btn_row, text="✕ Remover",
                   style="Danger.TButton",
                   command=self._remove_task).pack(side="left")

    # ------------------------------------------------------------------ SUBJ
    def _build_subjects_tab(self):
        parent = self.tab_subjects

        form = tk.Frame(parent, bg="#1A1D2E", pady=16, padx=20)
        form.pack(fill="x", pady=(0, 12))

        tk.Label(form, text="Nova Disciplina", bg="#1A1D2E", fg="#6C63FF",
                 font=("Georgia", 13, "bold")).grid(row=0, column=0,
                                                    columnspan=4, sticky="w",
                                                    pady=(0, 10))

        lbl = lambda t: tk.Label(form, text=t, bg="#1A1D2E", fg="#94A3B8",
                                 font=("Courier New", 9))
        ent = lambda w=22: tk.Entry(form, width=w, bg="#252840", fg="#E2E8F0",
                                    insertbackground="#E2E8F0",
                                    font=("Courier New", 10), relief="flat",
                                    bd=4)

        lbl("Nome *").grid(row=1, column=0, sticky="w")
        self.subj_name = ent()
        self.subj_name.grid(row=1, column=1, padx=(4, 12))

        lbl("Professor").grid(row=1, column=2, sticky="w")
        self.subj_teacher = ent()
        self.subj_teacher.grid(row=1, column=3, padx=(4, 12))

        lbl("Cor (hex)").grid(row=2, column=0, sticky="w", pady=(8, 0))
        self.subj_color = ent(10)
        self.subj_color.insert(0, "#6C63FF")
        self.subj_color.grid(row=2, column=1, sticky="w", padx=(4, 12),
                             pady=(8, 0))

        ttk.Button(form, text="+ Adicionar", style="Accent.TButton",
                   command=self._add_subject).grid(row=2, column=3,
                                                   padx=(4, 0), pady=(8, 0))

        cols = ("name", "teacher", "color", "tasks")
        self.subj_tree = ttk.Treeview(parent, columns=cols, show="headings",
                                      height=16)
        for col, head, w in [
            ("name", "Nome", 200),
            ("teacher", "Professor", 180),
            ("color", "Cor", 100),
            ("tasks", "Tarefas", 80),
        ]:
            self.subj_tree.heading(col, text=head)
            self.subj_tree.column(col, width=w, anchor="w")

        sb2 = ttk.Scrollbar(parent, orient="vertical",
                            command=self.subj_tree.yview)
        self.subj_tree.configure(yscrollcommand=sb2.set)
        self.subj_tree.pack(side="left", fill="both", expand=True)
        sb2.pack(side="left", fill="y")

        btn_row = tk.Frame(self.tab_subjects, bg="#0F1117")
        btn_row.pack(fill="x", pady=8)
        ttk.Button(btn_row, text="✕ Remover disciplina",
                   style="Danger.TButton",
                   command=self._remove_subject).pack(side="left")

    # ------------------------------------------------------------------ SUMM
    def _build_summary_tab(self):
        parent = self.tab_summary
        self.summary_frame = tk.Frame(parent, bg="#0F1117")
        self.summary_frame.pack(fill="both", expand=True, padx=8, pady=8)
        ttk.Button(parent, text="↻ Atualizar resumo", style="Accent.TButton",
                   command=self._refresh_summary).pack(pady=8)
        self._refresh_summary()

    # ------------------------------------------------------------------ LOGIC
    def _add_task(self):
        title = self.task_title.get().strip()
        if not title:
            messagebox.showwarning("Atenção", "O título é obrigatório.")
            return

        due_str = self.task_due.get().strip()
        due_date = None
        if due_str:
            try:
                due_date = datetime.strptime(due_str, "%d/%m/%Y").date().isoformat()
            except ValueError:
                messagebox.showwarning("Atenção",
                                       "Prazo inválido. Use DD/MM/AAAA.")
                return

        task = Task(
            title=title,
            subject=self.task_subject_var.get(),
            due=due_date,
            priority=self.task_priority.get(),
            notes=self.task_notes.get().strip(),
        )
        self.storage.add_task(task)
        self._save_data()
        self._refresh_task_list()
        self._clear_task_form()

    def _remove_task(self):
        sel = self.task_tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Selecione uma tarefa para remover.")
            return
        idx = self.task_tree.index(sel[0])
        self.storage.remove_task(idx)
        self._save_data()
        self._refresh_task_list()

    def _toggle_task(self):
        sel = self.task_tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Selecione uma tarefa.")
            return
        idx = self.task_tree.index(sel[0])
        self.storage.toggle_task(idx)
        self._save_data()
        self._refresh_task_list()

    def _add_subject(self):
        name = self.subj_name.get().strip()
        if not name:
            messagebox.showwarning("Atenção", "O nome é obrigatório.")
            return
        subj = Subject(
            name=name,
            teacher=self.subj_teacher.get().strip(),
            color=self.subj_color.get().strip() or "#6C63FF",
        )
        self.storage.add_subject(subj)
        self._save_data()
        self._refresh_subject_list()
        self._refresh_task_subjects_combo()
        self.subj_name.delete(0, "end")
        self.subj_teacher.delete(0, "end")

    def _remove_subject(self):
        sel = self.subj_tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Selecione uma disciplina.")
            return
        idx = self.subj_tree.index(sel[0])
        self.storage.remove_subject(idx)
        self._save_data()
        self._refresh_subject_list()
        self._refresh_task_subjects_combo()

    # ------------------------------------------------------------------ REFRESH
    def _refresh_task_list(self):
        for row in self.task_tree.get_children():
            self.task_tree.delete(row)
        for task in self.storage.tasks:
            status = "✔ Concluída" if task.done else "⏳ Pendente"
            self.task_tree.insert(
                "", "end",
                values=(task.title, task.subject, task.due or "—",
                        task.priority, status),
                tags=("done",) if task.done else (),
            )
        self.task_tree.tag_configure("done", foreground="#64748B")
        self._refresh_summary()

    def _refresh_subject_list(self):
        for row in self.subj_tree.get_children():
            self.subj_tree.delete(row)
        for subj in self.storage.subjects:
            count = sum(1 for t in self.storage.tasks
                        if t.subject == subj.name)
            self.subj_tree.insert(
                "", "end",
                values=(subj.name, subj.teacher or "—", subj.color, count),
            )

    def _refresh_task_subjects_combo(self):
        names = [s.name for s in self.storage.subjects]
        self.task_subject_combo["values"] = names

    def _refresh_summary(self):
        for w in self.summary_frame.winfo_children():
            w.destroy()

        tasks = self.storage.tasks
        total = len(tasks)
        done = sum(1 for t in tasks if t.done)
        pending = total - done
        overdue = sum(
            1 for t in tasks
            if not t.done and t.due and t.due < date.today().isoformat()
        )

        stats = [
            ("Total de tarefas", total, "#94A3B8"),
            ("Concluídas", done, "#22C55E"),
            ("Pendentes", pending, "#F59E0B"),
            ("Atrasadas", overdue, "#EF4444"),
        ]

        row_frame = tk.Frame(self.summary_frame, bg="#0F1117")
        row_frame.pack(fill="x", pady=(8, 20))

        for label, value, color in stats:
            card = tk.Frame(row_frame, bg="#1A1D2E", padx=24, pady=16)
            card.pack(side="left", padx=10)
            tk.Label(card, text=str(value), bg="#1A1D2E", fg=color,
                     font=("Georgia", 32, "bold")).pack()
            tk.Label(card, text=label, bg="#1A1D2E", fg="#94A3B8",
                     font=("Courier New", 9)).pack()

        # Tarefas por disciplina
        tk.Label(self.summary_frame, text="Tarefas por disciplina",
                 bg="#0F1117", fg="#6C63FF",
                 font=("Georgia", 13, "bold")).pack(anchor="w", padx=10)

        for subj in self.storage.subjects:
            subj_tasks = [t for t in tasks if t.subject == subj.name]
            if not subj_tasks:
                continue
            subj_done = sum(1 for t in subj_tasks if t.done)
            line = tk.Frame(self.summary_frame, bg="#1A1D2E", pady=8, padx=16)
            line.pack(fill="x", padx=10, pady=3)
            tk.Label(line, text=subj.name, bg="#1A1D2E", fg="#E2E8F0",
                     font=("Courier New", 11, "bold"), width=20,
                     anchor="w").pack(side="left")
            tk.Label(
                line,
                text=f"{subj_done}/{len(subj_tasks)} concluídas",
                bg="#1A1D2E", fg="#94A3B8",
                font=("Courier New", 10),
            ).pack(side="left", padx=16)

    def _clear_task_form(self):
        self.task_title.delete(0, "end")
        self.task_due.delete(0, "end")
        self.task_notes.delete(0, "end")
        self.task_priority.set("Média")

    # ------------------------------------------------------------------ I/O
    def _load_data(self):
        self.storage.load()
        self._refresh_task_list()
        self._refresh_subject_list()
        self._refresh_task_subjects_combo()

    def _save_data(self):
        self.storage.save()


def main():
    root = tk.Tk()
    EstudaFlowApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
