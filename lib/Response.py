"""
response
speak with program
"""
import tkinter as tk
from tkinter import scrolledtext


class ResponseFrame(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, text="ответы", *args, **kwargs)
        self._padx = 20
        self._pady = 10
        self.create_widgets()

    def create_widgets(self):
        self.response_text = scrolledtext.ScrolledText(self, width=50, height=10)
        self.response_text.grid(row=0, column=0, padx=self._padx, pady=self._pady)

    def write_response(self, message):
        self.response_text.insert(tk.END, message + "\n")
        self.response_text.see(tk.END)
