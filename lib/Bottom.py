"""
bottom
"""
import tkinter as tk


class ButtonFrame(tk.Frame):
    def __init__(self, parent, response_frame, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.response_frame = response_frame
        self.create_widgets()

    def create_widgets(self):
        confirm_button = tk.Button(self, text="Confirm", command=self.confirm)
        reset_button = tk.Button(self, text="Reset", command=self.reset)

        confirm_button.grid(row=0, column=0, padx=5, pady=5)
        reset_button.grid(row=0, column=1, padx=5, pady=5)

    def confirm(self):
        # Add logic to handle the confirm action
        message = "Confirm button pressed"
        self.response_frame.write_response(message)

    def reset(self):
        # Add logic to handle the reset action
        message = "Reset button pressed"
        self.response_frame.write_response(message)
