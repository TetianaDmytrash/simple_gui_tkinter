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
        self._padx = 6
        self._pady = 5
        self._bottom_limit_step = 0
        self._bottom_limit_period = 1
        self._bottom_limit_min_time = 250
        self._upper_limit_int_long = 110
        self._upper_limit_int = 65000
        self.engines_info = []
        self.create_widgets(number)

    def create_widgets(self, number):
        steps_label = tk.Label(self, text="шаги")
        period_label = tk.Label(self, text="период")
        time_label = tk.Label(self, text="мин время")

        steps_label.grid(row=0, column=1, padx=self._padx, pady=self._pady)
        period_label.grid(row=0, column=2, padx=self._padx, pady=self._pady)
        time_label.grid(row=0, column=3, padx=self._padx, pady=self._pady)

        for num in range(number):
            num_write = num + 1
            label = tk.Label(self, text=f"двигатель {num_write}")
            step_spinbox = tk.Spinbox(self, from_=self._bottom_limit_step, to=self._upper_limit_int_long)
            period_spinbox = tk.Spinbox(self, from_=self._bottom_limit_period, to=self._upper_limit_int)
            min_time_spinbox = tk.Spinbox(self, from_=self._bottom_limit_min_time, to=self._upper_limit_int)
            send_info_button = tk.Button(self, text="отправить", command=self.send_info)

            label.grid(row=num_write, column=0, padx=self._padx, pady=self._pady)
            step_spinbox.grid(row=num_write, column=1, padx=self._padx, pady=self._pady)
            period_spinbox.grid(row=num_write, column=2, padx=self._padx, pady=self._pady)
            min_time_spinbox.grid(row=num_write, column=3, padx=self._padx, pady=self._pady)
            send_info_button.grid(row=num_write, column=4, padx=self._padx, pady=self._pady)
            self.engines_info.append((str(num_write), step_spinbox.get(), period_spinbox.get()))

        print(f"in channel: {self.engines_info}")

    def get_step_period_info(self):
        return self.engines_info

    def send_info(self):
        print(f"#send info message")
