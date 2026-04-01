import numpy as np


class MotionModel:
    """
    Математична модель руху (Model).
    """

    def __init__(self, velocity, angle_deg, gravity=9.81):
        self.velocity = velocity
        self.angle = np.deg2rad(angle_deg)
        self.g = gravity

    def compute_main_params(self):
        t_total = (2 * self.velocity * np.sin(self.angle)) / self.g
        distance = (self.velocity ** 2 * np.sin(2 * self.angle)) / self.g
        height = (self.velocity ** 2 * (np.sin(self.angle) ** 2)) / (2 * self.g)
        return t_total, distance, height

    def build_path(self, steps=150):
        t_total, _, _ = self.compute_main_params()

        time = np.linspace(0, t_total, steps)

        x = self.velocity * np.cos(self.angle) * time
        y = self.velocity * np.sin(self.angle) * time - 0.5 * self.g * time**2

        y[y < 0] = 0

        return time, x, y