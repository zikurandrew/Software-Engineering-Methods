"""
GUI — відповідає за рендеринг елементів керування та динамічну
побудову таблиці станів DP.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from controller import Controller
from data_provider import DataProvider
from solvers import ALL_SOLVERS


# ─────────────────────────────────────────────
#  Палітра та шрифти
# ─────────────────────────────────────────────
C = {
    "bg":         "#1a1a2e",
    "panel":      "#16213e",
    "card":       "#0f3460",
    "accent":     "#e94560",
    "accent2":    "#533483",
    "text":       "#eaeaea",
    "text_dim":   "#8892a4",
    "success":    "#00b894",
    "header_bg":  "#533483",
    "tbl_odd":    "#0f3460",
    "tbl_even":   "#16213e",
    "tbl_head":   "#e94560",
    "tbl_path":   "#00b894",
}

F = {
    "title":  ("Consolas", 18, "bold"),
    "header": ("Consolas", 11, "bold"),
    "label":  ("Consolas", 10),
    "mono":   ("Consolas", 10),
    "big":    ("Consolas", 14, "bold"),
    "cell":   ("Consolas",  9),
    "small":  ("Consolas",  9, "bold"),
}


# ─────────────────────────────────────────────
#  Головне вікно
# ─────────────────────────────────────────────
class KnapsackApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Knapsack Problem Solver — Варіант №19")
        self.configure(bg=C["bg"])
        self.resizable(True, True)
        self.minsize(860, 660)

        self._ctrl = Controller(DataProvider())
        self._build_ui()
        self._reset_defaults()

    # ── Побудова інтерфейсу ───────────────────────────────────
    def _build_ui(self):
        self._build_titlebar()
        main = tk.Frame(self, bg=C["bg"])
        main.pack(fill="both", expand=True, padx=12, pady=12)
        self._build_left_panel(main)
        self._build_right_panel(main)

    def _build_titlebar(self):
        bar = tk.Frame(self, bg=C["header_bg"], pady=10)
        bar.pack(fill="x")
        tk.Label(bar, text="⚙  KNAPSACK PROBLEM SOLVER",
                 font=F["title"], bg=C["header_bg"], fg=C["text"]).pack()
        tk.Label(bar, text="Варіант №19  |  5 алгоритмів  |  Python + tkinter",
                 font=F["label"], bg=C["header_bg"], fg=C["text_dim"]).pack()

    # ── Ліва панель: введення + вибір ────────────────────────
    def _build_left_panel(self, parent):
        left = tk.Frame(parent, bg=C["panel"])
        left.pack(side="left", fill="y", padx=(0, 12), ipadx=10, ipady=10)

        self._section(left, "ВХІДНІ ДАНІ")

        fields = [
            ("Місткість рюкзака (W):",     "cap_var"),
            ("Ваги предметів (через ,):",   "weights_var"),
            ("Цінності предметів (через ,):", "values_var"),
        ]
        for lbl, attr in fields:
            self._input_row(left, lbl, attr)

        self._section(left, "АЛГОРИТМ")

        self.algo_var = tk.IntVar(value=0)
        for i, name in enumerate(self._ctrl.solver_names()):
            tk.Radiobutton(
                left, text=name, variable=self.algo_var, value=i,
                font=F["label"], bg=C["panel"], fg=C["text"],
                selectcolor=C["card"],
                activebackground=C["panel"], activeforeground=C["accent"],
                command=lambda idx=i: self._ctrl.set_solver(idx),
            ).pack(anchor="w", padx=10, pady=1)

        tk.Frame(left, bg=C["panel"], height=10).pack()

        tk.Button(
            left, text="▶  ЗАПУСТИТИ",
            font=F["header"], bg=C["accent"], fg="white",
            relief="flat", bd=0, padx=16, pady=8,
            activebackground="#c0392b", activeforeground="white",
            cursor="hand2", command=self._on_run,
        ).pack(fill="x", padx=8, pady=4)

        tk.Button(
            left, text="↺  Скинути до варіанту №19",
            font=F["label"], bg=C["panel"], fg=C["text_dim"],
            relief="flat", bd=0, cursor="hand2",
            command=self._reset_defaults,
        ).pack(fill="x", padx=8)

    def _input_row(self, parent, label: str, attr: str):
        tk.Label(parent, text=label, font=F["label"],
                 bg=C["panel"], fg=C["text_dim"], anchor="w").pack(
            fill="x", padx=8)
        var = tk.StringVar()
        setattr(self, attr, var)
        tk.Entry(parent, textvariable=var, font=F["mono"],
                 bg=C["card"], fg=C["text"],
                 insertbackground=C["accent"], relief="flat", bd=4,
                 ).pack(fill="x", padx=8, pady=(0, 6))

    # ── Права панель: результати ──────────────────────────────
    def _build_right_panel(self, parent):
        right = tk.Frame(parent, bg=C["bg"])
        right.pack(side="left", fill="both", expand=True)

        # Картка-резюме
        card = tk.Frame(right, bg=C["card"], pady=10, padx=14)
        card.pack(fill="x", pady=(0, 8))

        self.lbl_algo   = tk.Label(card, text="",
                                   font=F["label"], bg=C["card"],
                                   fg=C["text_dim"])
        self.lbl_algo.pack(anchor="w")

        self.lbl_result = tk.Label(
            card, text="Оберіть алгоритм та натисніть ▶ ЗАПУСТИТИ",
            font=F["big"], bg=C["card"], fg=C["text"])
        self.lbl_result.pack(anchor="w")

        self.lbl_time = tk.Label(card, text="",
                                 font=F["label"], bg=C["card"],
                                 fg=C["text_dim"])
        self.lbl_time.pack(anchor="w")

        # Текстовий звіт
        self._section(right, "ДЕТАЛЬНИЙ ЗВІТ")
        self.log = scrolledtext.ScrolledText(
            right, font=F["mono"], bg=C["panel"], fg=C["text"],
            insertbackground=C["accent"], relief="flat", bd=4,
            height=10, state="disabled", wrap="word")
        self.log.pack(fill="both", expand=True, pady=(2, 8))

        # Контейнер DP-таблиці (прихований до запуску DP)
        self._dp_header = tk.Label(
            right, text="  МАТРИЦЯ СТАНІВ — Динамічне програмування",
            font=F["header"], bg=C["card"], fg=C["accent"], anchor="w")
        self._dp_outer = tk.Frame(right, bg=C["bg"])

    # ── Обробники подій ───────────────────────────────────────
    def _on_run(self):
        try:
            self._ctrl.load_inputs(
                self.cap_var.get(),
                self.weights_var.get(),
                self.values_var.get())
        except ValueError as e:
            messagebox.showerror("Помилка вхідних даних", f"❌  {e}")
            return

        self._ctrl.set_solver(self.algo_var.get())
        result = self._ctrl.run()

        slv = self._ctrl.current_solver
        dp  = self._ctrl.dp

        self.lbl_algo.config(text=f"Алгоритм:  {slv.name}")
        self.lbl_result.config(
            text=f"Максимальна цінність:  {result.max_value}",
            fg=C["success"])
        self.lbl_time.config(
            text=f"Час виконання:  {result.elapsed_ms:.4f} мс")

        self._write_log(self._ctrl.build_report(result))
        self._refresh_dp_table(result)

    def _reset_defaults(self):
        self._ctrl.reset_to_defaults()
        dp = self._ctrl.dp
        self.cap_var.set(str(dp.capacity))
        self.weights_var.set(", ".join(map(str, dp.weights)))
        self.values_var.set(", ".join(map(str, dp.values)))

    # ── Лог ───────────────────────────────────────────────────
    def _write_log(self, text: str):
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.insert("end", text)
        self.log.config(state="disabled")

    # ── DP таблиця ────────────────────────────────────────────
    def _refresh_dp_table(self, result):
        """Показує або ховає DP-таблицю залежно від алгоритму."""
        self._dp_header.pack_forget()
        self._dp_outer.pack_forget()
        for w in self._dp_outer.winfo_children():
            w.destroy()

        if self.algo_var.get() != 3 or not result.extra:
            return

        self._dp_header.pack(fill="x", pady=(4, 0))
        self._dp_outer.pack(fill="both", expand=False, pady=(2, 0))
        self._render_dp_table(result.extra["table"], result.selected)

    def _render_dp_table(self, table: list[list[int]], selected: list[int]):
        dp = self._ctrl.dp
        n, W = dp.n, dp.capacity

        # Обчислення клітинок оптимального шляху
        path: set[tuple[int, int]] = set()
        j = W
        for i in range(n, 0, -1):
            path.add((i, j))
            if table[i][j] != table[i - 1][j]:
                j -= dp.weights[i - 1]
        path.add((0, j))

        # Canvas + scrollbars
        container = tk.Frame(self._dp_outer, bg=C["bg"])
        container.pack(fill="both", expand=True)

        vsb = ttk.Scrollbar(container, orient="vertical")
        hsb = ttk.Scrollbar(container, orient="horizontal")
        canvas = tk.Canvas(container, bg=C["panel"], height=200,
                           yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.config(command=canvas.yview)
        hsb.config(command=canvas.xview)
        vsb.pack(side="right",  fill="y")
        hsb.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=C["panel"])
        canvas.create_window((0, 0), window=inner, anchor="nw")

        # Заголовок: ємності 0..W
        tk.Label(inner, text="i\\W", font=F["small"],
                 bg=C["tbl_head"], fg="white",
                 width=5, relief="flat", bd=1,
                 ).grid(row=0, column=0, sticky="nsew", padx=1, pady=1)

        for j in range(W + 1):
            tk.Label(inner, text=str(j), font=F["small"],
                     bg=C["tbl_head"], fg="white",
                     width=3, relief="flat", bd=1,
                     ).grid(row=0, column=j + 1, sticky="nsew",
                            padx=1, pady=1)

        # Рядки даних
        for i in range(n + 1):
            if i == 0:
                row_lbl = "i=0"
            else:
                row_lbl = f"{i}(w{dp.weights[i-1]},v{dp.values[i-1]})"
            is_chosen = (i > 0) and ((i - 1) in selected)
            lbl_fg = C["tbl_path"] if is_chosen else C["text_dim"]

            tk.Label(inner, text=row_lbl, font=F["small"],
                     bg=C["tbl_head"], fg=lbl_fg,
                     relief="flat", bd=1,
                     ).grid(row=i + 1, column=0, sticky="nsew",
                            padx=1, pady=1)

            for j in range(W + 1):
                in_path = (i, j) in path
                bg = (C["tbl_path"]  if in_path else
                      C["tbl_odd"]   if i % 2 == 0 else C["tbl_even"])
                fg = C["bg"] if in_path else C["text"]
                tk.Label(inner, text=str(table[i][j]),
                         font=F["cell"], bg=bg, fg=fg,
                         width=3, relief="flat", bd=1,
                         ).grid(row=i + 1, column=j + 1,
                                sticky="nsew", padx=1, pady=1)

        inner.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    # ── Утиліта ───────────────────────────────────────────────
    @staticmethod
    def _section(parent, title: str):
        tk.Label(parent, text=f"  {title}", font=F["header"],
                 bg=C["card"], fg=C["accent"], anchor="w").pack(
            fill="x", pady=(10, 4))
