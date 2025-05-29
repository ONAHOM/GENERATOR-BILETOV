import os
from random import choice
import tkinter as tk
from tkinter import ttk, messagebox

class QuizApp(tk.Tk):
    def __init__(self, subjects_folder="subjects"):
        super().__init__()
        self.title(choice(["ЕБАНЫЙ КОРЕНЬ", "ХУЁВАЯ ОПТИМИЗАЦИЯЮ", "ДРОЧИЛЬНЯ v2.0", "ГОВНОЧИСТКА", "СЕРВЕР — ПИДОР", "АВТОМАТИЗАЦИЯ ХУЙНИ", "СИМУЛЯТОР ДОЛБОЁБА", "ПИЗДЮЛИМ ВСЕХ", "ХУЙНЯ, НО ПРИКОЛЬНАЯ", "ПОШЛО ВСЁ НАХУЙ", "СПАСИБО, ЧТО ЖИВОЙ", "НАЖМИ F, ЧТОБЫ ВЫЙТИ", "СИНТАКСИЧЕСКИЙ ПОНОС", "ХУЙ ЗНАЕТ, КАК ЭТО РАБОТАЕТ"]))
        self.geometry("600x400")

        self.subjects_folder = subjects_folder
        self.files = []
        self.questions = []
        self.remaining = []
        self.current_ticket = []
        self.num_per_ticket = 0

        # Build UI
        self._build_selection_frame()
        self._refresh_file_list()

    def _refresh_file_list(self):
        self.files = self._get_subject_files()
        menu = self.file_menu["menu"]
        menu.delete(0, "end")
        for file in self.files:
            menu.add_command(label=file, command=lambda value=file: self.file_var.set(value))
        if self.files:
            self.file_var.set(self.files[0])

    def _get_subject_files(self):
        if not os.path.isdir(self.subjects_folder):
            messagebox.showerror("Error", f"Папка '{self.subjects_folder}' не найдена.")
            self.destroy()
            return []
        files = [f for f in os.listdir(self.subjects_folder)
                 if os.path.isfile(os.path.join(self.subjects_folder, f)) and not f.startswith('.')]
        return files

    def _build_selection_frame(self):
        self.selection_frame = ttk.Frame(self)
        self.selection_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        ttk.Label(self.selection_frame, text="Выбери файл с темами:").grid(row=0, column=0, sticky=tk.W)
        self.file_var = tk.StringVar()
        self.file_menu = ttk.OptionMenu(self.selection_frame, self.file_var, "")
        self.file_menu.grid(row=0, column=1, sticky=tk.W)

        refresh_btn = ttk.Button(self.selection_frame, text="Обновить", command=self._refresh_file_list)
        refresh_btn.grid(row=0, column=2, padx=10)

        ttk.Label(self.selection_frame, text="Вопросов в билет:").grid(row=1, column=0, sticky=tk.W)
        self.num_entry = ttk.Entry(self.selection_frame, width=5)
        self.num_entry.grid(row=1, column=1, sticky=tk.W)

        start_btn = ttk.Button(self.selection_frame, text="НАЧАТЬ СТРАДАТЬ", command=self._start_quiz)
        start_btn.grid(row=2, column=0, columnspan=3, pady=10)

    def _start_quiz(self):
        selected = self.file_var.get()
        if not selected:
            messagebox.showwarning("Warning", "Выбери файл.")
            return
        try:
            n = int(self.num_entry.get())
            if n < 1:
                raise ValueError
            self.num_per_ticket = n
        except ValueError:
            messagebox.showwarning("Warning", "Введи число вопросов в билете.")
            return

        path = os.path.join(self.subjects_folder, selected)
        try:
            with open(path, encoding='utf-8') as f:
                lines = [ln.strip() for ln in f if ln.strip()]
        except Exception as e:
            messagebox.showerror("Error", f"Неудалось прочитать: {e}")
            return

        self.questions = lines
        self.remaining = list(self.questions)
        self.selection_frame.destroy()
        self._build_quiz_frame()
        self._show_ticket()

    def _build_quiz_frame(self):
        self.quiz_frame = ttk.Frame(self)
        self.quiz_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.question_text = tk.Text(self.quiz_frame, height=15, wrap=tk.WORD)
        self.question_text.pack(fill=tk.BOTH, expand=True)

        btn_frame = ttk.Frame(self.quiz_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Знаю", command=self._next_ticket).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Заебался", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def _show_ticket(self):
        if not self.remaining:
            messagebox.showinfo("Красава", "Все вопросы разобраны!")
            self.destroy()
            return

        # Choose questions
        self.current_ticket = []
        for _ in range(self.num_per_ticket):
            if not self.remaining:
                break
            q = choice(self.remaining)
            self.current_ticket.append(q)
            self.remaining.remove(q)

        # Display
        self.question_text.config(state=tk.NORMAL)
        self.question_text.delete("1.0", tk.END)
        for idx, q in enumerate(self.current_ticket, 1):
            original_index = self.questions.index(q) + 1
            self.question_text.insert(tk.END, f"{idx}. {q} (номер вопроса {original_index})\n\n")
        count_left = len(self.remaining)
        self.question_text.insert(tk.END, f"Осталось вопросов: {count_left}")
        self.question_text.config(state=tk.DISABLED)

    def _next_ticket(self):
        self._show_ticket()

if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()