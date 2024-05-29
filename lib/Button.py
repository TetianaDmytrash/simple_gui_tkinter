"""
bottom
"""
import tkinter as tk

from lib.SpeakChannel import SpeakCOMPort


class ButtonFrame(tk.Frame):
    def __init__(self, parent, port_controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.port_controller = port_controller
        self.create_widgets()

    def create_widgets(self):
        open_port_button = tk.Button(self, text="открыть порт", command=self.port_controller.open_channel)
        # reset_button = tk.Button(self, text="Reset", command=self.reset)

        open_port_button.grid(row=0, column=0, padx=5, pady=5)
        # reset_button.grid(row=0, column=1, padx=5, pady=5)

    def reset(self):
        # Add logic to handle the reset action
        message = "Reset button pressed"
        self.response_frame.write_response(message)
