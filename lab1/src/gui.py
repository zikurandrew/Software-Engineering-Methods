import tkinter as tk
from tkinter import colorchooser, messagebox
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from physics import calculate_motion


class MotionApp:

    def __init__(self, root):
        self.root = root
        root.title("Motion simulation")

        root.geometry("500x400")
        root.resizable(True, True)
        root.configure(bg="white")

        self.color = "blue"

        tk.Label(root, text="x0", font=("Arial", 12)).grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.x0 = tk.Entry(root, font=("Arial", 12))
        self.x0.grid(row=0, column=1, padx=20, pady=10)

        tk.Label(root, text="y0", font=("Arial", 12)).grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.y0 = tk.Entry(root, font=("Arial", 12))
        self.y0.grid(row=1, column=1, padx=20, pady=10)

        tk.Label(root, text="angle", font=("Arial", 12)).grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.angle = tk.Entry(root, font=("Arial", 12))
        self.angle.grid(row=2, column=1, padx=20, pady=10)

        tk.Label(root, text="v0", font=("Arial", 12)).grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.v0 = tk.Entry(root, font=("Arial", 12))
        self.v0.grid(row=3, column=1, padx=20, pady=10)

        tk.Label(root, text="a", font=("Arial", 12)).grid(row=4, column=0, padx=20, pady=10, sticky="w")
        self.a = tk.Entry(root, font=("Arial", 12))
        self.a.grid(row=4, column=1, padx=20, pady=10)

        tk.Button(root, text="Choose color",
                  command=self.choose_color,
                  font=("Arial", 12),
                  width=15).grid(row=5, column=0, padx=20, pady=15)

        tk.Button(root, text="Build graph",
                  command=self.build_graph,
                  font=("Arial", 12),
                  width=15).grid(row=5, column=1, padx=20, pady=15)

        tk.Button(root, text="Clear",
                  command=self.clear_graph,
                  font=("Arial", 12),
                  width=15).grid(row=6, column=0, columnspan=2, pady=10)

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.color = color

    def build_graph(self):

        try:
            x0 = float(self.x0.get())
            y0 = float(self.y0.get())
            v0 = float(self.v0.get())
            angle = float(self.angle.get())
            a = float(self.a.get())

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers")
            return

        x, y = calculate_motion(x0, y0, v0, angle, a)

        fig, ax = plt.subplots()

        ax.plot(x, y, color=self.color, label="Trajectory")

        ax.scatter(x0, y0, color="green", s=80, label="Start")

        point, = ax.plot([], [], 'ro')

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Trajectory of motion")

        ax.grid(True)
        ax.axhline(0)
        ax.axvline(0)

        ax.axis("equal")

        ax.legend()

        def update(frame):
            point.set_data([x[frame]], [y[frame]])
            return point,

        ani = animation.FuncAnimation(
            fig,
            update,
            frames=len(x),
            interval=40,
            blit=True
        )

        plt.show()

    def clear_graph(self):
        plt.clf()