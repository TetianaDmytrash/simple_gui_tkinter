"""
set the starting configuration for displaying fields for entering periods and steps
"""
import tkinter as tk


class StepsAndPeriodFrame(tk.LabelFrame):
    """
    paint frame with name, steps and period
    """

    def __init__(self, parent, number, *args, **kwargs):
        super().__init__(parent, text="шаги и период", *args, **kwargs)
        self._padx = 10
        self._pady = 5
        self._bottom_limit_step = 10
        self._bottom_limit_period = 5
        self._upper_limit = 110
        self.create_widgets(number)

    def create_widgets(self, number):
        steps_label = tk.Label(self, text="шаги")
        period_label = tk.Label(self, text="период")

        steps_label.grid(row=0, column=1, padx=self._padx, pady=self._pady)
        period_label.grid(row=0, column=2, padx=self._padx, pady=self._pady)

        for num in range(number):
            num_write = num + 1
            label = tk.Label(self, text=f"станок {num_write}")
            step_spinbox = tk.Spinbox(self, from_=self._bottom_limit_step, to=self._upper_limit)
            period_spinbox = tk.Spinbox(self, from_=self._bottom_limit_period, to=self._upper_limit)

            label.grid(row=num_write, column=0, padx=self._padx, pady=self._pady)
            step_spinbox.grid(row=num_write, column=1, padx=self._padx, pady=self._pady)
            period_spinbox.grid(row=num_write, column=2, padx=self._padx, pady=self._pady)

