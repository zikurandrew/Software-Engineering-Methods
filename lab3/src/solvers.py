"""
Computational Core — п'ять солверів задачі про рюкзак.
Кожен клас реалізує інтерфейс .solve(DataProvider) → KnapsackResult.
"""

import time
from data_provider import DataProvider


class KnapsackResult:
    def __init__(self, max_value: int, selected: list[int],
                 elapsed_ms: float, extra=None):
        self.max_value  = max_value
        self.selected   = selected   # індекси обраних предметів (0-based)
        self.elapsed_ms = elapsed_ms
        self.extra      = extra      # напр. {"table": ...} для DP


# ──────────────────────────────────────────────────────────────
#  Метод 1 — Груба сила  O(2ⁿ)
# ──────────────────────────────────────────────────────────────
class BruteForceSolver:
    name       = "Груба сила (Brute Force)"
    complexity = "O(2ⁿ)"

    def solve(self, dp: DataProvider) -> KnapsackResult:
        t0 = time.perf_counter()
        best_val, best_sel = 0, []

        for mask in range(1 << dp.n):
            sel = [i for i in range(dp.n) if mask & (1 << i)]
            w   = sum(dp.weights[i] for i in sel)
            v   = sum(dp.values[i]  for i in sel)
            if w <= dp.capacity and v > best_val:
                best_val, best_sel = v, sel

        elapsed = (time.perf_counter() - t0) * 1000
        return KnapsackResult(best_val, best_sel, elapsed)


# ──────────────────────────────────────────────────────────────
#  Метод 2 — Рекурсивний  O(2ⁿ)
# ──────────────────────────────────────────────────────────────
class RecursiveSolver:
    name       = "Рекурсивний метод"
    complexity = "O(2ⁿ)"

    def solve(self, dp: DataProvider) -> KnapsackResult:
        t0 = time.perf_counter()
        w, v, W = dp.weights, dp.values, dp.capacity

        def rec(i: int, rem: int) -> int:
            if i == 0 or rem == 0:
                return 0
            if w[i - 1] > rem:
                return rec(i - 1, rem)
            return max(rec(i - 1, rem),
                       v[i - 1] + rec(i - 1, rem - w[i - 1]))

        best_val = rec(dp.n, W)

        def backtrack(i: int, rem: int) -> list[int]:
            if i == 0 or rem == 0:
                return []
            if w[i - 1] > rem:
                return backtrack(i - 1, rem)
            without = rec(i - 1, rem)
            with_   = v[i - 1] + rec(i - 1, rem - w[i - 1])
            if with_ >= without:
                return backtrack(i - 1, rem - w[i - 1]) + [i - 1]
            return backtrack(i - 1, rem)

        selected = backtrack(dp.n, W)
        elapsed  = (time.perf_counter() - t0) * 1000
        return KnapsackResult(best_val, selected, elapsed)


# ──────────────────────────────────────────────────────────────
#  Метод 3 — Жадібний  O(n log n)
# ──────────────────────────────────────────────────────────────
class GreedySolver:
    name       = "Жадібний алгоритм"
    complexity = "O(n log n)"

    def solve(self, dp: DataProvider) -> KnapsackResult:
        t0 = time.perf_counter()
        ratio = sorted(range(dp.n),
                       key=lambda i: dp.values[i] / dp.weights[i],
                       reverse=True)
        rem, val, sel = dp.capacity, 0, []
        for i in ratio:
            if dp.weights[i] <= rem:
                rem -= dp.weights[i]
                val += dp.values[i]
                sel.append(i)

        elapsed = (time.perf_counter() - t0) * 1000
        return KnapsackResult(val, sorted(sel), elapsed)


# ──────────────────────────────────────────────────────────────
#  Метод 4 — Динамічне програмування  O(n·W)
# ──────────────────────────────────────────────────────────────
class DynamicProgrammingSolver:
    name       = "Динамічне програмування"
    complexity = "O(n·W)"

    def solve(self, dp: DataProvider) -> KnapsackResult:
        t0 = time.perf_counter()
        n, W = dp.n, dp.capacity
        w, v = dp.weights, dp.values

        # Побудова матриці (n+1) × (W+1)
        table = [[0] * (W + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(W + 1):
                table[i][j] = table[i - 1][j]
                if w[i - 1] <= j:
                    candidate = v[i - 1] + table[i - 1][j - w[i - 1]]
                    if candidate > table[i][j]:
                        table[i][j] = candidate

        best_val = table[n][W]

        # Відновлення набору предметів
        j, sel = W, []
        for i in range(n, 0, -1):
            if table[i][j] != table[i - 1][j]:
                sel.append(i - 1)
                j -= w[i - 1]
        sel.reverse()

        elapsed = (time.perf_counter() - t0) * 1000
        return KnapsackResult(best_val, sel, elapsed,
                              extra={"table": table})


# ──────────────────────────────────────────────────────────────
#  Метод 5 — Гілки і межі  O(2ⁿ) з відсіканням
# ──────────────────────────────────────────────────────────────
class BranchAndBoundSolver:
    name       = "Метод гілок і меж"
    complexity = "O(2ⁿ) з відсіканням гілок"

    def solve(self, dp: DataProvider) -> KnapsackResult:
        t0 = time.perf_counter()
        n, W = dp.n, dp.capacity

        # Сортуємо за питомою цінністю для ефективної верхньої оцінки
        order = sorted(range(n),
                       key=lambda i: dp.values[i] / dp.weights[i],
                       reverse=True)
        w = [dp.weights[i] for i in order]
        v = [dp.values[i]  for i in order]

        def upper_bound(idx: int, rem: int, cur_val: float) -> float:
            ub = cur_val
            for k in range(idx, n):
                if w[k] <= rem:
                    rem -= w[k]
                    ub  += v[k]
                else:
                    ub += v[k] * rem / w[k]
                    break
            return ub

        best = [0, []]

        def bnb(idx: int, rem: int, cur_val: int, chosen: list[int]):
            if cur_val > best[0]:
                best[0] = cur_val
                best[1] = chosen[:]
            if idx == n:
                return
            if upper_bound(idx, rem, cur_val) <= best[0]:
                return  # відсікання неефективної гілки

            if w[idx] <= rem:                           # беремо предмет
                chosen.append(order[idx])
                bnb(idx + 1, rem - w[idx], cur_val + v[idx], chosen)
                chosen.pop()

            bnb(idx + 1, rem, cur_val, chosen)          # не беремо предмет

        bnb(0, W, 0, [])
        elapsed = (time.perf_counter() - t0) * 1000
        return KnapsackResult(best[0], sorted(best[1]), elapsed)


# ──────────────────────────────────────────────────────────────
#  Реєстр солверів (порядок відповідає індексам у GUI)
# ──────────────────────────────────────────────────────────────
ALL_SOLVERS = [
    BruteForceSolver(),
    RecursiveSolver(),
    GreedySolver(),
    DynamicProgrammingSolver(),
    BranchAndBoundSolver(),
]
