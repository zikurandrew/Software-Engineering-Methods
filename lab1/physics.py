import numpy as np

def calculate_motion(x0, y0, v0, angle, a):

    t = np.linspace(0, 10, 200)

    angle_rad = np.radians(angle)

    vx = v0 * np.cos(angle_rad)
    vy = v0 * np.sin(angle_rad)

    x = x0 + vx * t + (a * t**2) / 2
    y = y0 + vy * t

    return x, y