"""
Data Provider — підготовка та зберігання вхідних параметрів задачі.
"""


class DataProvider:
    DEFAULT_CAPACITY = 23
    DEFAULT_WEIGHTS  = [9, 9, 9, 7, 8, 9]
    DEFAULT_VALUES   = [9, 3, 15, 14, 8, 5]

    def __init__(self):
        self.capacity: int       = self.DEFAULT_CAPACITY
        self.weights:  list[int] = self.DEFAULT_WEIGHTS[:]
        self.values:   list[int] = self.DEFAULT_VALUES[:]

    @property
    def n(self) -> int:
        return len(self.weights)

    def load_from_strings(self, cap_str: str, w_str: str, v_str: str):
        """Парсинг та валідація вхідних рядків. Кидає ValueError при помилці."""
        cap = int(cap_str.strip())
        if cap <= 0:
            raise ValueError("Місткість рюкзака має бути > 0")

        weights = [int(x.strip()) for x in w_str.split(",")]
        values  = [int(x.strip()) for x in v_str.split(",")]

        if len(weights) != len(values):
            raise ValueError("Масиви ваг та цінностей мають однакову довжину")
        if any(wt <= 0 for wt in weights):
            raise ValueError("Всі ваги мають бути > 0")
        if any(v < 0 for v in values):
            raise ValueError("Цінності не можуть бути від'ємними")

        self.capacity = cap
        self.weights  = weights
        self.values   = values
