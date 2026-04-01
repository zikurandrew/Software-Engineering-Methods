import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation


class MotionView:
    """
    Відповідає за інтерфейс і відображення.
    """

    def __init__(self, root, start_cb, clear_cb):
        self.root = root
        self.root.title("Projectile Simulator")
        self.root.geometry("1000x600")

        # Layout
        self.left = tk.Frame(root)
        self.left.pack(side="left", fill="both", expand=True)

        self.right = tk.Frame(root, bg="#2c2f33", width=280)
        self.right.pack(side="right", fill="y")

        # Plot
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.left)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Controls
        self._build_controls(start_cb, clear_cb)

        self.animation = None
        self._init_plot()

    def _build_controls(self, start_cb, clear_cb):
        style = {"bg": "#2c2f33", "fg": "white"}

        tk.Label(self.right, text="Параметри", font=("Arial", 14, "bold"), **style).pack(pady=15)

        tk.Label(self.right, text="Швидкість:", **style).pack(anchor="w", padx=10)
        self.speed = tk.Entry(self.right)
        self.speed.insert(0, "25")
        self.speed.pack(fill="x", padx=10, pady=5)

        tk.Label(self.right, text="Кут:", **style).pack(anchor="w", padx=10)
        self.angle = tk.Entry(self.right)
        self.angle.insert(0, "45")
        self.angle.pack(fill="x", padx=10, pady=5)

        ttk.Button(self.right, text="Запустити", command=start_cb).pack(fill="x", padx=10, pady=10)
        ttk.Button(self.right, text="Очистити", command=clear_cb).pack(fill="x", padx=10)

        self.output = tk.Label(self.right, text="", **style, justify="left")
        self.output.pack(padx=10, pady=20)

    def get_values(self):
        return self.speed.get(), self.angle.get()

    def show_error(self, msg):
        messagebox.showerror("Помилка", msg)

    def display_info(self, t, d, h):
        self.output.config(text=f"t = {t:.2f} c\nL = {d:.2f} м\nH = {h:.2f} м")

    def _init_plot(self):
        self.ax.clear()
        self.ax.set_title("Траєкторія руху")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.grid()

        self.line, = self.ax.plot([], [])
        self.dot, = self.ax.plot([], [], 'ro')

        self.canvas.draw()

    def animate(self, t, x, y):
        if self.animation:
            self.animation.event_source.stop()

        self._init_plot()

        self.ax.set_xlim(0, max(x) * 1.1)
        self.ax.set_ylim(0, max(y) * 1.2)

        def step(i):
            self.line.set_data(x[:i], y[:i])
            self.dot.set_data([x[i]], [y[i]])
            return self.line, self.dot

        self.animation = FuncAnimation(self.fig, step, frames=len(x), interval=30, repeat=False)
        self.canvas.draw()

    def clear(self):
        if self.animation is not None and self.animation.event_source is not None:
            self.animation.event_source.stop()

        self.animation = None
        self._init_plot()
        self.output.config(text="")