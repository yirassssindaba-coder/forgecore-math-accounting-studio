import os
import time
import webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Any, Dict, List, Optional

from core import ForgeCoreEngine

APP_NAME = "ForgeCore Math & Accounting Studio"

THEME = {
    "bg": "#0a1020",
    "panel": "#111a33",
    "panel2": "#162446",
    "accent": "#7c5cff",
    "accent2": "#31d2ff",
    "text": "#f4f7ff",
    "muted": "#9fb3d9",
    "success": "#7ff0ae",
    "warn": "#ffd166",
    "danger": "#ff6b6b",
}

try:
    import winsound  # Windows only
except Exception:
    winsound = None


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.engine = ForgeCoreEngine()

        self.root.title(APP_NAME)
        self.root.geometry("1380x880")
        self.root.minsize(1180, 780)
        self.root.configure(bg=THEME["bg"])

        self.quiz_session: Optional[Dict[str, Any]] = None
        self.current_qid: Optional[int] = None
        self.current_choice = tk.StringVar(value="")
        self.timer_job: Optional[str] = None

        self.metro_on = tk.BooleanVar(value=False)
        self.metro_bpm = tk.IntVar(value=72)
        self.metro_job: Optional[str] = None

        self._configure_style()
        self._build_header()
        self._build_body()
        self._refresh_sidebar()
        self._tick_clock()
        self._tick_vibe()

    # -----------------------------
    # Style + helpers
    # -----------------------------
    def _configure_style(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        # Base
        style.configure("TFrame", background=THEME["bg"])
        style.configure("TLabel", background=THEME["bg"], foreground=THEME["text"])
        style.configure("TNotebook", background=THEME["bg"], borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background=THEME["panel"],
            foreground=THEME["muted"],
            padding=(14, 8),
            borderwidth=0,
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", THEME["panel2"]), ("active", THEME["panel2"])],
            foreground=[("selected", THEME["text"]), ("active", THEME["text"])],
        )

        style.configure("Accent.TButton", background=THEME["accent"], foreground="#ffffff", padding=(10, 8), borderwidth=0)
        style.map("Accent.TButton", background=[("active", "#6847f5")])
        style.configure("Ghost.TButton", background=THEME["panel2"], foreground=THEME["text"], padding=(10, 8), borderwidth=0)
        style.map("Ghost.TButton", background=[("active", "#1d2f58")])

        # Entries / combo: avoid white fields
        style.configure("TEntry", fieldbackground="#0d1730", foreground=THEME["text"])
        style.configure("TCombobox", fieldbackground="#0d1730", background=THEME["panel2"], foreground=THEME["text"])
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", "#0d1730")],
            foreground=[("readonly", THEME["text"])],
        )
        self.root.option_add("*TCombobox*Listbox.background", "#0d1730")
        self.root.option_add("*TCombobox*Listbox.foreground", THEME["text"])
        self.root.option_add("*TCombobox*Listbox.selectBackground", THEME["accent"])
        self.root.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")

        style.configure("Treeview", background="#0d1730", fieldbackground="#0d1730", foreground=THEME["text"], rowheight=28)
        style.configure("Treeview.Heading", background=THEME["panel2"], foreground=THEME["text"], relief="flat")
        style.map("Treeview.Heading", background=[("active", THEME["accent"])])

    def _panel(self, master: tk.Widget, bg: str = THEME["panel"]) -> tk.Frame:
        return tk.Frame(master, bg=bg, highlightbackground="#223766", highlightthickness=1)

    def _section_title(self, master: tk.Widget, text: str, bg: Optional[str] = None) -> None:
        bg = bg if bg is not None else master["bg"]
        tk.Label(master, text=text, font=("Segoe UI", 13, "bold"), fg=THEME["text"], bg=bg).pack(anchor="w", pady=(0, 10))

    def _open_folder(self, path: str) -> None:
        try:
            if os.name == "nt":
                os.startfile(path)  # type: ignore[attr-defined]
            else:
                webbrowser.open(path)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # -----------------------------
    # Header + sidebar vibe
    # -----------------------------
    def _build_header(self) -> None:
        frame = tk.Frame(self.root, bg=THEME["bg"], height=94)
        frame.pack(fill="x", padx=18, pady=(18, 10))
        frame.pack_propagate(False)

        brand = tk.Frame(frame, bg=THEME["bg"])
        brand.pack(side="left", fill="y")
        tk.Label(brand, text="ForgeCore", font=("Segoe UI", 26, "bold"), fg=THEME["text"], bg=THEME["bg"]).pack(anchor="w")
        tk.Label(
            brand,
            text="Nuansa menghitung: kalkulator rumus + quiz 1000 soal + music focus playlist",
            font=("Segoe UI", 10),
            fg=THEME["accent2"],
            bg=THEME["bg"],
        ).pack(anchor="w", pady=(2, 0))

        right = tk.Frame(frame, bg=THEME["bg"])
        right.pack(side="right")

        self.clock_var = tk.StringVar(value=time.strftime("%H:%M:%S"))
        self.status_var = tk.StringVar(value="READY")

        for text_var, width in ((self.status_var, 18), (self.clock_var, 10)):
            box = tk.Frame(right, bg=THEME["panel"], highlightbackground="#223766", highlightthickness=1)
            box.pack(side="left", padx=(10, 0))
            tk.Label(box, textvariable=text_var, width=width, font=("Consolas", 11, "bold"), fg=THEME["text"], bg=THEME["panel"]).pack(padx=14, pady=10)

    def _build_body(self) -> None:
        shell = tk.Frame(self.root, bg=THEME["bg"])
        shell.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        # Sidebar
        left = tk.Frame(shell, bg=THEME["panel"], width=320, highlightbackground="#223766", highlightthickness=1)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        tk.Label(left, text="Counting Dashboard", font=("Segoe UI", 16, "bold"), fg=THEME["text"], bg=THEME["panel"]).pack(anchor="w", padx=18, pady=(18, 8))

        self.lbl_mastered = tk.Label(left, text="-", font=("Segoe UI", 18, "bold"), fg=THEME["text"], bg=THEME["panel"])
        self.lbl_mastered.pack(anchor="w", padx=18, pady=(0, 4))
        self.lbl_accuracy = tk.Label(left, text="-", font=("Segoe UI", 11), fg=THEME["muted"], bg=THEME["panel"])
        self.lbl_accuracy.pack(anchor="w", padx=18, pady=(0, 10))

        vibe = self._panel(left, bg="#0d1730")
        vibe.pack(fill="x", padx=16, pady=(0, 10))
        tk.Label(vibe, text="Math vibe", font=("Segoe UI", 10), fg=THEME["muted"], bg="#0d1730").pack(anchor="w", padx=14, pady=(10, 0))
        self.vibe_var = tk.StringVar(value="7×8 = 56")
        tk.Label(vibe, textvariable=self.vibe_var, font=("Consolas", 16, "bold"), fg=THEME["accent2"], bg="#0d1730").pack(anchor="w", padx=14, pady=(2, 10))

        tk.Label(left, text="Quick actions", font=("Segoe UI", 14, "bold"), fg=THEME["text"], bg=THEME["panel"]).pack(anchor="w", padx=18, pady=(6, 8))
        ttk.Button(left, text="Open storage folder", style="Ghost.TButton", command=lambda: self._open_folder(self.engine.storage_dir)).pack(fill="x", padx=16, pady=5)
        ttk.Button(left, text="Open Learning Hub", style="Accent.TButton", command=lambda: self.notebook.select(self.tab_learning)).pack(fill="x", padx=16, pady=5)
        ttk.Button(left, text="Reset quiz mastery (danger)", style="Ghost.TButton", command=self.reset_mastery).pack(fill="x", padx=16, pady=5)

        # Main content
        center = tk.Frame(shell, bg=THEME["bg"])
        center.pack(side="left", fill="both", expand=True, padx=(14, 0))

        self.notebook = ttk.Notebook(center)
        self.notebook.pack(fill="both", expand=True)

        self.tab_calc = tk.Frame(self.notebook, bg=THEME["bg"])
        self.tab_quiz = tk.Frame(self.notebook, bg=THEME["bg"])
        self.tab_learning = tk.Frame(self.notebook, bg=THEME["bg"])
        self.tab_music = tk.Frame(self.notebook, bg=THEME["bg"])

        self.notebook.add(self.tab_calc, text="Super Calculator")
        self.notebook.add(self.tab_quiz, text="Quiz Arena")
        self.notebook.add(self.tab_learning, text="Learning Hub")
        self.notebook.add(self.tab_music, text="Music & Focus")

        self._build_calc_tab()
        self._build_quiz_tab()
        self._build_learning_tab()
        self._build_music_tab()

    def _tick_clock(self) -> None:
        self.clock_var.set(time.strftime("%H:%M:%S"))
        self.root.after(1000, self._tick_clock)

    def _tick_vibe(self) -> None:
        # lightweight "counting vibe" rotation
        import random
        a = random.randint(2, 19)
        b = random.randint(2, 19)
        op = random.choice(["×", "+", "−"])
        if op == "×":
            val = a * b
        elif op == "+":
            val = a + b
        else:
            val = a - b
        self.vibe_var.set(f"{a}{op}{b} = {val}")
        self.root.after(1200, self._tick_vibe)

    def _refresh_sidebar(self) -> None:
        mastered = sum(1 for i in range(1, 1001) if self.engine.is_mastered(i))
        attempted = int(self.engine.quiz_stats.get("attempted", 0) or 0)
        correct = int(self.engine.quiz_stats.get("correct", 0) or 0)
        acc = (correct / attempted * 100.0) if attempted else 0.0
        self.lbl_mastered.config(text=f"Mastered: {mastered}/1000")
        self.lbl_accuracy.config(text=f"Lifetime accuracy: {acc:.1f}%  (correct {correct} / attempted {attempted})")

    def reset_mastery(self) -> None:
        if messagebox.askyesno("Reset", "Reset semua mastery? (soal akan muncul lagi)"):
            self.engine.quiz_mastered = {}
            self.engine.quiz_stats = {"attempted": 0, "correct": 0}
            self.engine.save()
            self._refresh_sidebar()
            messagebox.showinfo("Done", "Mastery di-reset.")

    # -----------------------------
    # Calculator tab
    # -----------------------------
    def _build_calc_tab(self) -> None:
        shell = tk.Frame(self.tab_calc, bg=THEME["bg"])
        shell.pack(fill="both", expand=True, padx=14, pady=14)

        left = self._panel(shell)
        left.pack(side="left", fill="y", padx=(0, 12))
        left.configure(width=370)
        left.pack_propagate(False)

        self._section_title(left, "Formula library", bg=THEME["panel"])

        # Treeview with categories
        self.formula_tree = ttk.Treeview(left, columns=("name",), show="tree")
        self.formula_tree.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.formulas = self.engine.formula_catalog()
        self.formula_by_id = {f["id"]: f for f in self.formulas}

        cats: Dict[str, str] = {}
        for f in self.formulas:
            cat = f.get("category", "Other")
            if cat not in cats:
                cats[cat] = self.formula_tree.insert("", "end", text=cat, open=True)
            self.formula_tree.insert(cats[cat], "end", text=f.get("name", f["id"]), values=(f["id"],))

        self.formula_tree.bind("<<TreeviewSelect>>", self._on_formula_select)

        right = self._panel(shell)
        right.pack(side="left", fill="both", expand=True)

        self.calc_title = tk.Label(right, text="Pilih formula di kiri", font=("Segoe UI", 16, "bold"), fg=THEME["text"], bg=THEME["panel"])
        self.calc_title.pack(anchor="w", padx=16, pady=(16, 6))

        self.calc_desc = tk.Label(right, text="—", font=("Segoe UI", 10), fg=THEME["muted"], bg=THEME["panel"], wraplength=880, justify="left")
        self.calc_desc.pack(anchor="w", padx=16, pady=(0, 10))

        self.inputs_frame = tk.Frame(right, bg=THEME["panel"])
        self.inputs_frame.pack(fill="x", padx=16, pady=(0, 10))

        self.btn_compute = ttk.Button(right, text="Compute", style="Accent.TButton", command=self.compute_selected_formula)
        self.btn_compute.pack(anchor="w", padx=16, pady=(0, 10))

        self.result_box = tk.Text(right, height=12, bg="#0d1730", fg=THEME["text"], insertbackground=THEME["text"], borderwidth=0, wrap="word")
        self.result_box.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        self.result_box.insert("1.0", "Result akan muncul di sini.\n")
        self.result_box.configure(state="disabled")

        self.selected_formula_id: Optional[str] = None
        self.input_vars: Dict[str, tk.StringVar] = {}

    def _on_formula_select(self, _evt: Any) -> None:
        sel = self.formula_tree.selection()
        if not sel:
            return
        item = sel[0]
        parent = self.formula_tree.parent(item)
        if parent == "":
            return  # category clicked
        fid = (self.formula_tree.item(item, "values") or [""])[0]
        if not fid:
            return
        self.selected_formula_id = fid
        meta = self.formula_by_id.get(fid, {})
        self.calc_title.config(text=str(meta.get("name", fid)))
        self.calc_desc.config(text=str(meta.get("category", "")))

        # rebuild inputs
        for w in list(self.inputs_frame.winfo_children()):
            w.destroy()
        self.input_vars.clear()

        inputs = meta.get("inputs", [])
        for i, inp in enumerate(inputs):
            row = tk.Frame(self.inputs_frame, bg=THEME["panel"])
            row.pack(fill="x", pady=4)
            tk.Label(row, text=str(inp.get("label", inp.get("k"))), font=("Segoe UI", 10), fg=THEME["muted"], bg=THEME["panel"]).pack(side="left")
            var = tk.StringVar(value=str(inp.get("default", "")))
            self.input_vars[str(inp.get("k"))] = var
            ent = ttk.Entry(row, textvariable=var)
            ent.pack(side="right", fill="x", expand=True, padx=(10, 0))
        self._write_result(f"Selected: {meta.get('name', fid)}\n")

    def compute_selected_formula(self) -> None:
        if not self.selected_formula_id:
            messagebox.showinfo("Info", "Pilih formula dulu.")
            return
        inputs = {k: v.get() for k, v in self.input_vars.items()}
        self.status_var.set("COMPUTING")
        res = self.engine.compute_formula(self.selected_formula_id, inputs)
        if res.get("ok"):
            self._write_result(f"✅ {self.formula_by_id[self.selected_formula_id].get('name', self.selected_formula_id)}\n"
                               f"Steps: {res.get('steps','-')}\n"
                               f"Result: {res.get('result')}\n")
            self._soft_tick()
        else:
            self._write_result(f"❌ Error: {res.get('error')}\n")
        self.status_var.set("READY")
        self._refresh_sidebar()

    def _write_result(self, text: str) -> None:
        self.result_box.configure(state="normal")
        self.result_box.insert("end", text + "\n")
        self.result_box.see("end")
        self.result_box.configure(state="disabled")

    def _soft_tick(self) -> None:
        # tiny feedback sound for "counting vibe"
        if winsound:
            try:
                winsound.Beep(880, 60)
            except Exception:
                pass

    # -----------------------------
    # Quiz tab
    # -----------------------------
    def _build_quiz_tab(self) -> None:
        shell = tk.Frame(self.tab_quiz, bg=THEME["bg"])
        shell.pack(fill="both", expand=True, padx=14, pady=14)

        top = self._panel(shell)
        top.pack(fill="x", pady=(0, 12))
        top_inner = tk.Frame(top, bg=THEME["panel"])
        top_inner.pack(fill="x", padx=16, pady=14)

        self._section_title(top_inner, "Quiz setup", bg=THEME["panel"])

        row = tk.Frame(top_inner, bg=THEME["panel"])
        row.pack(fill="x")

        self.quiz_subject = tk.StringVar(value="Campur")
        self.quiz_count = tk.StringVar(value="20")
        self.quiz_minutes = tk.StringVar(value="15")
        self.hide_mastered = tk.BooleanVar(value=True)

        def _label(master, t):
            tk.Label(master, text=t, font=("Segoe UI", 10), fg=THEME["muted"], bg=THEME["panel"]).pack(side="left", padx=(0, 8))

        _label(row, "Subject")
        ttk.Combobox(row, textvariable=self.quiz_subject, values=["Campur", "Matematika", "Akuntansi"], state="readonly", width=14).pack(side="left", padx=(0, 16))

        _label(row, "Jumlah soal")
        ttk.Combobox(row, textvariable=self.quiz_count, values=["5","10","20","30","50","100"], state="readonly", width=10).pack(side="left", padx=(0, 16))

        _label(row, "Menit")
        ttk.Combobox(row, textvariable=self.quiz_minutes, values=["5","10","15","20","30","45","60"], state="readonly", width=10).pack(side="left", padx=(0, 16))

        tk.Checkbutton(row, text="Hide mastered", variable=self.hide_mastered, bg=THEME["panel"], fg=THEME["text"], selectcolor="#0d1730", activebackground=THEME["panel"], activeforeground=THEME["text"]).pack(side="left", padx=(0, 16))

        ttk.Button(row, text="Start Quiz", style="Accent.TButton", command=self.start_quiz).pack(side="right")

        # Content
        body = tk.Frame(shell, bg=THEME["bg"])
        body.pack(fill="both", expand=True)

        left = self._panel(body)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))

        header = tk.Frame(left, bg=THEME["panel"])
        header.pack(fill="x", padx=16, pady=(14, 8))
        self.quiz_progress_var = tk.StringVar(value="No quiz running.")
        self.quiz_timer_var = tk.StringVar(value="--:--")
        tk.Label(header, textvariable=self.quiz_progress_var, font=("Segoe UI", 12, "bold"), fg=THEME["text"], bg=THEME["panel"]).pack(side="left")
        tk.Label(header, textvariable=self.quiz_timer_var, font=("Consolas", 12, "bold"), fg=THEME["accent2"], bg=THEME["panel"]).pack(side="right")

        self.quiz_qtext = tk.Text(left, height=8, bg="#0d1730", fg=THEME["text"], insertbackground=THEME["text"], borderwidth=0, wrap="word")
        self.quiz_qtext.pack(fill="x", padx=16, pady=(0, 10))
        self.quiz_qtext.configure(state="disabled")

        self.options_frame = tk.Frame(left, bg=THEME["panel"])
        self.options_frame.pack(fill="both", expand=True, padx=16, pady=(0, 10))

        # Buttons
        btns = tk.Frame(left, bg=THEME["panel"])
        btns.pack(fill="x", padx=16, pady=(0, 16))
        ttk.Button(btns, text="Submit", style="Accent.TButton", command=self.submit_answer).pack(side="left")
        ttk.Button(btns, text="Skip", style="Ghost.TButton", command=self.skip_question).pack(side="left", padx=(10, 0))
        ttk.Button(btns, text="End Quiz", style="Ghost.TButton", command=self.end_quiz).pack(side="right")

        right = self._panel(body)
        right.pack(side="left", fill="y")
        right.configure(width=330)
        right.pack_propagate(False)

        self._section_title(right, "Session stats", bg=THEME["panel"])
        self.lbl_session = tk.Label(right, text="—", font=("Consolas", 11), fg=THEME["text"], bg=THEME["panel"], justify="left")
        self.lbl_session.pack(anchor="w", padx=16, pady=(0, 12))

        self.feedback = tk.Text(right, height=18, bg="#0d1730", fg=THEME["text"], insertbackground=THEME["text"], borderwidth=0, wrap="word")
        self.feedback.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        self.feedback.insert("1.0", "Feedback akan muncul di sini.\n")
        self.feedback.configure(state="disabled")

    def start_quiz(self) -> None:
        try:
            count = int(self.quiz_count.get())
            minutes = int(self.quiz_minutes.get())
        except Exception:
            messagebox.showerror("Error", "Jumlah soal dan menit harus angka.")
            return
        subject = self.quiz_subject.get().strip()
        sess = self.engine.build_quiz_session(subject, count, minutes, bool(self.hide_mastered.get()))
        if not sess.get("ok"):
            messagebox.showinfo("Info", sess.get("error", "Gagal memulai quiz."))
            return
        self.quiz_session = sess
        self.status_var.set("QUIZ_RUNNING")
        self.current_choice.set("")
        self._load_question_at_index(0)
        self._tick_timer()

    def _load_question_at_index(self, idx: int) -> None:
        if not self.quiz_session:
            return
        queue = self.quiz_session.get("queue", [])
        if idx >= len(queue):
            self.end_quiz()
            return
        qid = int(queue[idx])
        q = self.engine.get_question_by_id(qid)
        if not q:
            self.end_quiz()
            return

        self.quiz_session["index"] = idx
        self.current_qid = qid
        self.current_choice.set("")

        self.quiz_progress_var.set(f"Q {idx+1}/{len(queue)}  •  {q.subject}  •  ID {qid}")
        self._set_text(self.quiz_qtext, q.prompt)

        for w in list(self.options_frame.winfo_children()):
            w.destroy()

        for letter in ["A", "B", "C", "D"]:
            text = q.options.get(letter, "")
            rb = tk.Radiobutton(
                self.options_frame,
                text=f"{letter}. {text}",
                variable=self.current_choice,
                value=letter,
                bg=THEME["panel"],
                fg=THEME["text"],
                selectcolor="#0d1730",
                activebackground=THEME["panel2"],
                activeforeground=THEME["text"],
                anchor="w",
                justify="left",
                wraplength=720,
                padx=8,
                pady=6,
            )
            rb.pack(fill="x", pady=4)

        self._update_session_stats()

    def _set_text(self, widget: tk.Text, text: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.configure(state="disabled")

    def _append_feedback(self, text: str) -> None:
        self.feedback.configure(state="normal")
        self.feedback.insert("end", text + "\n\n")
        self.feedback.see("end")
        self.feedback.configure(state="disabled")

    def submit_answer(self) -> None:
        if not self.quiz_session or self.current_qid is None:
            messagebox.showinfo("Info", "Tidak ada quiz yang berjalan.")
            return
        chosen = self.current_choice.get().strip().upper()
        if chosen not in ("A", "B", "C", "D"):
            messagebox.showinfo("Info", "Pilih jawaban A/B/C/D.")
            return
        qid = self.current_qid
        result = self.engine.grade_answer(qid, chosen)
        if not result.get("ok"):
            self._append_feedback("Error: " + str(result.get("error")))
            return

        self.quiz_session["attempted"] += 1
        if result.get("is_correct"):
            self.quiz_session["correct"] += 1
            self._append_feedback(f"✅ Q{qid} benar. Jawaban: {result.get('correct')}\nHint (kunci): {result.get('explanation')}")
            self._soft_tick()
        else:
            self.quiz_session["wrong"] += 1
            self._append_feedback(f"❌ Q{qid} salah. Kamu: {result.get('chosen')}  |  Benar: {result.get('correct')}\nHint (kunci): {result.get('explanation')}")
        self.quiz_session["answers"][str(qid)] = chosen
        self._refresh_sidebar()

        # next
        idx = int(self.quiz_session.get("index", 0)) + 1
        self._load_question_at_index(idx)

    def skip_question(self) -> None:
        if not self.quiz_session:
            return
        idx = int(self.quiz_session.get("index", 0)) + 1
        self._append_feedback("⏭️ Skipped.")
        self._load_question_at_index(idx)

    def _tick_timer(self) -> None:
        if not self.quiz_session:
            self.quiz_timer_var.set("--:--")
            return
        now = time.time()
        remaining = int(self.quiz_session["end_ts"] - now)
        if remaining <= 0:
            self.quiz_timer_var.set("00:00")
            self.end_quiz()
            return
        mm = remaining // 60
        ss = remaining % 60
        self.quiz_timer_var.set(f"{mm:02d}:{ss:02d}")
        self.timer_job = self.root.after(1000, self._tick_timer)

    def _update_session_stats(self) -> None:
        if not self.quiz_session:
            self.lbl_session.config(text="—")
            return
        s = self.quiz_session
        self.lbl_session.config(
            text=(
                f"Subject: {s.get('subject')}\n"
                f"Total: {s.get('count')}\n"
                f"Attempted: {s.get('attempted')}\n"
                f"Correct: {s.get('correct')}\n"
                f"Wrong: {s.get('wrong')}\n"
                f"Hide mastered: {bool(self.hide_mastered.get())}\n"
            )
        )

    def end_quiz(self) -> None:
        if self.timer_job:
            try:
                self.root.after_cancel(self.timer_job)
            except Exception:
                pass
            self.timer_job = None

        if not self.quiz_session:
            return
        s = self.quiz_session
        attempted = int(s.get("attempted", 0))
        correct = int(s.get("correct", 0))
        acc = (correct / attempted * 100.0) if attempted else 0.0
        self._append_feedback(f"🏁 Quiz selesai. Accuracy: {acc:.1f}% ({correct}/{attempted})")
        self.status_var.set("READY")
        self.quiz_session = None
        self.current_qid = None
        self.quiz_progress_var.set("No quiz running.")
        self.quiz_timer_var.set("--:--")
        self._update_session_stats()
        self._refresh_sidebar()

    # -----------------------------
    # Learning hub tab
    # -----------------------------
    def _build_learning_tab(self) -> None:
        shell = tk.Frame(self.tab_learning, bg=THEME["bg"])
        shell.pack(fill="both", expand=True, padx=14, pady=14)

        card = self._panel(shell)
        card.pack(fill="both", expand=True)

        inner = tk.Frame(card, bg=THEME["panel"])
        inner.pack(fill="both", expand=True, padx=16, pady=16)

        self._section_title(inner, "Built-in materials (PDF)", bg=THEME["panel"])
        tk.Label(
            inner,
            text="Kamu bisa open atau export/copy PDF ke folder pilihanmu.",
            font=("Segoe UI", 10),
            fg=THEME["muted"],
            bg=THEME["panel"],
        ).pack(anchor="w", pady=(0, 12))

        self.pdf_items = [
            ("materi-matematika-akuntansi-dan-1000-soal.pdf", "Materi Matematika + Akuntansi + 1000 soal + kunci"),
            ("panduan-matematika-sains-data-lengkap.pdf", "Panduan Matematika/Statistika untuk Sains Data (rumus + peta belajar)"),
            ("panduan-akuntansi-s1-s3-lengkap.pdf", "Panduan Akuntansi S1–S3 (rumus + peta kompetensi)"),
        ]

        for fname, desc in self.pdf_items:
            row = tk.Frame(inner, bg=THEME["panel"])
            row.pack(fill="x", pady=6)
            tk.Label(row, text=fname, font=("Consolas", 11, "bold"), fg=THEME["text"], bg=THEME["panel"]).pack(side="left")
            tk.Label(row, text=desc, font=("Segoe UI", 9), fg=THEME["muted"], bg=THEME["panel"]).pack(side="left", padx=(12, 0))
            ttk.Button(row, text="Open", style="Accent.TButton", command=lambda f=fname: self.open_pdf(f)).pack(side="right")
            ttk.Button(row, text="Export copy", style="Ghost.TButton", command=lambda f=fname: self.export_pdf(f)).pack(side="right", padx=(0, 10))

    def open_pdf(self, filename: str) -> None:
        src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", filename)
        try:
            if os.name == "nt":
                os.startfile(src)  # type: ignore[attr-defined]
            else:
                webbrowser.open(src)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_pdf(self, filename: str) -> None:
        dest = filedialog.asksaveasfilename(
            title="Save PDF as",
            initialfile=filename,
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
        )
        if not dest:
            return
        try:
            self.engine.export_resource_pdf(filename, dest)
            messagebox.showinfo("Saved", f"Saved to:\n{dest}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # -----------------------------
    # Music tab
    # -----------------------------
    def _build_music_tab(self) -> None:
        shell = tk.Frame(self.tab_music, bg=THEME["bg"])
        shell.pack(fill="both", expand=True, padx=14, pady=14)

        left = self._panel(shell)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))

        inner = tk.Frame(left, bg=THEME["panel"])
        inner.pack(fill="both", expand=True, padx=16, pady=16)
        self._section_title(inner, "Playlist (URL)", bg=THEME["panel"])

        self.playlist = tk.Listbox(inner, bg="#0d1730", fg=THEME["text"], selectbackground=THEME["accent"], selectforeground="#fff", height=10, borderwidth=0)
        self.playlist.pack(fill="x", pady=(0, 10))
        self._reload_playlist()

        form = tk.Frame(inner, bg=THEME["panel"])
        form.pack(fill="x", pady=(0, 10))
        self.track_title = tk.StringVar(value="")
        self.track_url = tk.StringVar(value="")
        ttk.Entry(form, textvariable=self.track_title).pack(side="left", fill="x", expand=True)
        ttk.Entry(form, textvariable=self.track_url).pack(side="left", fill="x", expand=True, padx=(10, 0))
        ttk.Button(form, text="Add", style="Accent.TButton", command=self.add_track).pack(side="left", padx=(10, 0))

        btns = tk.Frame(inner, bg=THEME["panel"])
        btns.pack(fill="x")
        ttk.Button(btns, text="Play (open URL)", style="Accent.TButton", command=self.play_selected).pack(side="left")
        ttk.Button(btns, text="Remove", style="Ghost.TButton", command=self.remove_selected).pack(side="left", padx=(10, 0))

        tip = tk.Label(
            inner,
            text="Catatan: URL dibuka dengan player default (browser/app). Ini paling stabil tanpa dependency tambahan.",
            font=("Segoe UI", 9),
            fg=THEME["muted"],
            bg=THEME["panel"],
            wraplength=780,
            justify="left",
        )
        tip.pack(anchor="w", pady=(10, 0))

        right = self._panel(shell)
        right.pack(side="left", fill="y")
        right.configure(width=340)
        right.pack_propagate(False)

        rinner = tk.Frame(right, bg=THEME["panel"])
        rinner.pack(fill="both", expand=True, padx=16, pady=16)

        self._section_title(rinner, "Focus Metronome", bg=THEME["panel"])
        tk.Label(
            rinner,
            text="Buat nuansa menghitung: tick stabil sesuai BPM (opsional).",
            font=("Segoe UI", 10),
            fg=THEME["muted"],
            bg=THEME["panel"],
            wraplength=300,
            justify="left",
        ).pack(anchor="w", pady=(0, 10))

        tk.Checkbutton(
            rinner,
            text="Enable metronome",
            variable=self.metro_on,
            bg=THEME["panel"],
            fg=THEME["text"],
            selectcolor="#0d1730",
            activebackground=THEME["panel"],
            activeforeground=THEME["text"],
            command=self.toggle_metronome,
        ).pack(anchor="w")

        tk.Label(rinner, text="BPM", font=("Segoe UI", 10), fg=THEME["muted"], bg=THEME["panel"]).pack(anchor="w", pady=(10, 0))
        tk.Scale(rinner, from_=40, to=180, orient="horizontal", variable=self.metro_bpm, bg=THEME["panel"], fg=THEME["text"], troughcolor="#0d1730", highlightthickness=0).pack(fill="x")

        self.metro_status = tk.Label(rinner, text="Metronome: OFF", font=("Consolas", 11, "bold"), fg=THEME["accent2"], bg=THEME["panel"])
        self.metro_status.pack(anchor="w", pady=(10, 0))

        tk.Label(
            rinner,
            text="Jika kamu mau audio yang benar-benar embedded di dalam app, kita bisa tambahkan opsi VLC/ffplay (butuh install).",
            font=("Segoe UI", 9),
            fg=THEME["muted"],
            bg=THEME["panel"],
            wraplength=300,
            justify="left",
        ).pack(anchor="w", pady=(12, 0))

    def _reload_playlist(self) -> None:
        self.playlist.delete(0, "end")
        for item in self.engine.music_playlist:
            self.playlist.insert("end", item.get("title", "Untitled"))

    def add_track(self) -> None:
        title = self.track_title.get().strip() or "Untitled"
        url = self.track_url.get().strip()
        try:
            self.engine.add_track(title, url)
            self.track_title.set("")
            self.track_url.set("")
            self._reload_playlist()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def remove_selected(self) -> None:
        sel = self.playlist.curselection()
        if not sel:
            return
        idx = int(sel[0])
        self.engine.remove_track(idx)
        self._reload_playlist()

    def play_selected(self) -> None:
        sel = self.playlist.curselection()
        if not sel:
            messagebox.showinfo("Info", "Pilih 1 track.")
            return
        idx = int(sel[0])
        try:
            url = self.engine.music_playlist[idx]["url"]
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def toggle_metronome(self) -> None:
        if self.metro_on.get():
            self.metro_status.config(text="Metronome: ON")
            self._metro_tick()
        else:
            self.metro_status.config(text="Metronome: OFF")
            if self.metro_job:
                try:
                    self.root.after_cancel(self.metro_job)
                except Exception:
                    pass
                self.metro_job = None

    def _metro_tick(self) -> None:
        if not self.metro_on.get():
            return
        bpm = max(40, min(180, int(self.metro_bpm.get() or 72)))
        interval_ms = int(60000 / bpm)
        if winsound:
            try:
                winsound.Beep(660, 45)
            except Exception:
                pass
        self.metro_job = self.root.after(interval_ms, self._metro_tick)


def main() -> None:
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
