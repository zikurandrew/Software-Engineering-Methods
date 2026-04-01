import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import messagebox

# ===== MODEL =====
def calculate(v0, angle, g=9.81):
    theta = np.radians(angle)
    
    t_flight = (2 * v0 * np.sin(theta)) / g
    t = np.linspace(0, t_flight, 200)
    
    x = v0 * np.cos(theta) * t
    y = v0 * np.sin(theta) * t - 0.5 * g * t**2
    
    H = (v0**2 * np.sin(theta)**2) / (2 * g)
    L = (v0**2 * np.sin(2 * theta)) / g
    
    return x, y, t, H, L, t_flight


# ===== VIEW =====
def animate(x, y, H, L):
    fig, ax = plt.subplots()
    
    ax.set_xlim(0, L * 1.1)
    ax.set_ylim(0, H * 1.2)
    ax.set_title("Projectile Motion")
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Height (m)")
    ax.grid()

    line, = ax.plot([], [], lw=2)
    point, = ax.plot([], [], 'ro')

    def update(frame):
        line.set_data(x[:frame], y[:frame])
        point.set_data(x[frame], y[frame])
        return line, point

    anim = FuncAnimation(fig, update, frames=len(x), interval=20)
    plt.show()


# ===== CONTROLLER =====
def run_simulation():
    try:
        v0 = float(entry_v0.get())
        angle = float(entry_angle.get())

        if v0 <= 0 or not (0 < angle < 90):
            raise ValueError

        x, y, t, H, L, t_flight = calculate(v0, angle)

        result_label.config(
            text=f"Time: {t_flight:.2f}s | Height: {H:.2f}m | Range: {L:.2f}m"
        )

        animate(x, y, H, L)

    except:
        messagebox.showerror("Error", "Invalid input!")


# ===== GUI =====
root = tk.Tk()
root.title("Projectile Simulator")
root.geometry("400x250")

tk.Label(root, text="Initial Speed (m/s)").pack()
entry_v0 = tk.Entry(root)
entry_v0.pack()

tk.Label(root, text="Angle (degrees)").pack()
entry_angle = tk.Entry(root)
entry_angle.pack()

tk.Button(root, text="Start Simulation", command=run_simulation).pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()