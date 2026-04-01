import tkinter as tk
from main import MotionModel
from gui import MotionView


class MotionController:
    """
    Контролер (зв'язок Model + View)
    """

    def __init__(self):
        self.root = tk.Tk()
        self.view = MotionView(self.root, self.start, self.clear)

    def start(self):
        v_str, a_str = self.view.get_values()

        try:
            v = float(v_str)
            a = float(a_str)

            if v <= 0 or not (0 < a < 90):
                raise ValueError
        except:
            self.view.show_error("Некоректні дані")
            return

        model = MotionModel(v, a)

        t, d, h = model.compute_main_params()
        self.view.display_info(t, d, h)

        t_arr, x_arr, y_arr = model.build_path()
        self.view.animate(t_arr, x_arr, y_arr)

    def clear(self):
        self.view.clear()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MotionController()
    app.run()