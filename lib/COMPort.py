"""
COM port
"""
import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports


class ChoosePortFrame(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, text="выбрать порт", *args, **kwargs)
        self._padx = 10
        self._pady = 5
        self.selected_port = None
        self.com_ports = self.find_com_ports_in_system()
        self.create_widgets(self.com_ports)

    def create_widgets(self, ports):
        port_label = tk.Label(self, text="порт")
        self.port_combobox = ttk.Combobox(self, values=ports)

        port_label.grid(row=1, column=1, padx=self._padx, pady=self._pady)
        self.port_combobox.grid(row=1, column=2, padx=self._padx, pady=self._pady)
        self.port_combobox.bind("<<ComboboxSelected>>", self.on_port_selected)

    def on_port_selected(self, event):
        self.selected_port = self.port_combobox.get()
        print(f"selected port: {self.selected_port}")

    def get_port(self):
        print(f"here: {self.selected_port}")
        return self.selected_port

    def find_com_ports_in_system(self):
        try:
            ports_name = list(serial.tools.list_ports.comports())
            print(f"COM ports exist in system: {ports_name}")
            if len(ports_name) == 0:
                print(f"didn`t find any COM ports. Do example list.")
                ports_name = ["", "COM", "COM7", "COM8"]
            return ports_name
        except Exception as e:
            print(f"error occurred during find COM ports: {e}")
