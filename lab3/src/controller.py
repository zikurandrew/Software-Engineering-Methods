"""
Controller — пов'язує вибір користувача з конкретним солвером.
"""

from data_provider import DataProvider
from solvers import ALL_SOLVERS, KnapsackResult


class Controller:
    def __init__(self, data_provider: DataProvider):
        self.dp            = data_provider
        self._solver_index = 0

    # ── Вибір алгоритму ───────────────────────────────────────
    def set_solver(self, index: int):
        if not 0 <= index < len(ALL_SOLVERS):
            raise IndexError(f"Індекс солвера {index} поза межами")
        self._solver_index = index

    @property
    def current_solver(self):
        return ALL_SOLVERS[self._solver_index]

    # ── Оновлення даних ───────────────────────────────────────
    def load_inputs(self, cap_str: str, w_str: str, v_str: str):
        """Делегує валідацію та збереження до DataProvider."""
        self.dp.load_from_strings(cap_str, w_str, v_str)

    def reset_to_defaults(self):
        self.dp.capacity = DataProvider.DEFAULT_CAPACITY
        self.dp.weights  = DataProvider.DEFAULT_WEIGHTS[:]
        self.dp.values   = DataProvider.DEFAULT_VALUES[:]

    # ── Виконання ─────────────────────────────────────────────
    def run(self) -> KnapsackResult:
        return self.current_solver.solve(self.dp)

    # ── Допоміжні геттери для GUI ─────────────────────────────
    def solver_names(self) -> list[str]:
        return [s.name for s in ALL_SOLVERS]

    def build_report(self, result: KnapsackResult) -> str:
        """Формує текстовий звіт про результат."""
        dp  = self.dp
        slv = self.current_solver
        sel = result.selected

        sel_str  = ", ".join(
            f"предмет {i+1} (w={dp.weights[i]}, v={dp.values[i]})"
            for i in sel) or "—"
        total_w  = sum(dp.weights[i] for i in sel)

        lines = [
            "─" * 54,
            f"  Алгоритм  : {slv.name}",
            f"  Складність : {slv.complexity}",
            f"  Місткість  : {dp.capacity}  |  Предметів: {dp.n}",
            "─" * 54,
            "  №    Вага   Цінність   Питома ціна",
        ]
        for i in range(dp.n):
            ratio = dp.values[i] / dp.weights[i]
            mark  = "  ◀ ОБРАНО" if i in sel else ""
            lines.append(
                f"  {i+1:2}.  {dp.weights[i]:5}  {dp.values[i]:8}  "
                f"{ratio:11.4f}{mark}"
            )
        lines += [
            "─" * 54,
            f"  Обрані    : {sel_str}",
            f"  Сума ваг  : {total_w} / {dp.capacity}",
            f"  Макс. цінність : {result.max_value}",
            f"  Час виконання  : {result.elapsed_ms:.4f} мс",
            "─" * 54,
        ]
        return "\n".join(lines)
