"""
.
"""
import tkinter as tk

from Bottom import ButtonFrame
from COMPort import ChoosePortFrame
from Response import ResponseFrame
from StepsAndPeriod import StepsAndPeriodFrame


class COMPortApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Speak with COM Port")
        self._padx = 20
        self._pady = 10
        # self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self)
        frame.pack()
        return frame

    def port_frame(self, frame):
        self.choose_port_frame = ChoosePortFrame(frame)
        self.choose_port_frame.grid(row=0, column=0, padx=self._padx, pady=self._pady)
        return self.choose_port_frame.get_port()

    def step_period_frame(self, frame):
        self.steps_period_frame = StepsAndPeriodFrame(frame, 4)
        self.steps_period_frame.grid(row=1, column=0, padx=self._padx, pady=self._pady)

    def speak_frame(self, frame):
        self.response_frame = ResponseFrame(frame)
        self.response_frame.grid(row=2, column=0, padx=self._padx, pady=self._pady)

    def press_button_frame(self, frame):
        self.button_frame = ButtonFrame(frame, self.response_frame)
        self.button_frame.grid(row=3, column=0, pady=10)



