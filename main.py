import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports
import threading
import json
import os

class SerialApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Serial Port Interface")
        
        self.config_file = "config.json"
        self.load_config()
        
        self.serial_connection = None
        self.read_thread = None
        self.stop_reading = False
        
        self.create_widgets(5)  # 5 двигателя по умолчанию
        
    def create_widgets(self, number):
        self.engines_info = []
        
        self.port_label = ttk.Label(self.root, text="Select COM Port:")
        self.port_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.port_var = tk.StringVar()
        self.port_combobox = ttk.Combobox(self.root, textvariable=self.port_var)
        self.port_combobox['values'] = self.get_serial_ports()
        self.port_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.port_combobox.bind('<<ComboboxSelected>>', self.connect_to_port)
        
        self.clear_config_button = ttk.Button(self.root, text="Clear Config", command=self.clear_config)
        self.clear_config_button.grid(row=0, column=4, padx=5, pady=5, sticky="e")
        
        self.data_text = tk.Text(self.root, height=15, width=50)
        self.data_text.grid(row=1, column=0, columnspan=5, padx=5, pady=5)
        
        self.send_all_button = ttk.Button(self.root, text="Send All", command=self.send_all_data)
        self.send_all_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.restart_button = ttk.Button(self.root, text="Restart", command=self.send_restart)
        self.restart_button.grid(row=2, column=2, columnspan=2, padx=5, pady=5)
        
        # Заголовки столбцов
        engine_label = ttk.Label(self.root, text="Engine")
        engine_label.grid(row=3, column=0, padx=5, pady=5)
        
        step_label = ttk.Label(self.root, text="Step")
        step_label.grid(row=3, column=1, padx=5, pady=5)
        
        period_label = ttk.Label(self.root, text="Period")
        period_label.grid(row=3, column=2, padx=5, pady=5)
        
        time_label = ttk.Label(self.root, text="Time")
        time_label.grid(row=3, column=3, padx=5, pady=5)
        
        for num in range(number):
            num_write = num + 1
            
            engine_num_label = ttk.Label(self.root, text=f"Engine {num_write}")
            engine_num_label.grid(row=num+4, column=0, padx=5, pady=5)
            
            step_var = tk.IntVar()
            step_entry = ttk.Entry(self.root, textvariable=step_var)
            step_entry.grid(row=num+4, column=1, padx=5, pady=5)
            
            period_var = tk.IntVar()
            period_entry = ttk.Entry(self.root, textvariable=period_var)
            period_entry.grid(row=num+4, column=2, padx=5, pady=5)
            
            time_var = tk.IntVar()
            time_entry = ttk.Entry(self.root, textvariable=time_var)
            time_entry.grid(row=num+4, column=3, padx=5, pady=5)
            
            send_button = ttk.Button(self.root, text=f"Send {num_write}", command=lambda num_write=num_write, step_var=step_var, period_var=period_var, time_var=time_var: self.send_data(num_write, step_var, period_var, time_var))
            send_button.grid(row=num+4, column=4, padx=5, pady=5)
            
            self.engines_info.append((step_var, period_var, time_var))
        
        self.load_previous_config()
    
    def get_serial_ports(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]
    
    def connect_to_port(self, event=None):
        try:
            if self.serial_connection:
                self.serial_connection.close()
            
            selected_port = self.port_var.get()
            if selected_port:
                self.serial_connection = serial.Serial(selected_port, baudrate=115200, timeout=1)
                self.stop_reading = False
                self.read_thread = threading.Thread(target=self.read_from_port)
                self.read_thread.start()
        except (serial.SerialException, OSError) as e:
            self.data_text.insert(tk.END, f"Error connecting to port: {e}\n")
            self.data_text.see(tk.END)
    
    def read_from_port(self):
        while not self.stop_reading:
            if self.serial_connection:
                try:
                    if self.serial_connection.in_waiting > 0:
                        data = self.serial_connection.readline().strip()
                        try:
                            decoded_data = data.decode('utf-8')
                        except UnicodeDecodeError:
                            decoded_data = str(data)  # Fallback to raw bytes representation
                        self.data_text.insert(tk.END, decoded_data + "\n")
                        self.data_text.see(tk.END)
                except (serial.SerialException, OSError) as e:
                    self.data_text.insert(tk.END, f"Error reading from port: {e}\n")
                    self.data_text.see(tk.END)
                    self.stop_reading = True
    
    def send_data(self, num_write, step_var, period_var, time_var):
        if self.serial_connection:
            try:
                step_value = step_var.get()
                period_value = period_var.get()
                time_value = time_var.get()
                data_to_send = f"set:{num_write};{step_value};{period_value}.{time_value}\n"
                self.serial_connection.write(data_to_send.encode('utf-8'))
            except (serial.SerialException, OSError) as e:
                self.data_text.insert(tk.END, f"Error sending data: {e}\n")
                self.data_text.see(tk.END)
    
    def send_all_data(self):
        for num_write, (step_var, period_var, time_var) in enumerate(self.engines_info, start=1):
            self.send_data(num_write, step_var, period_var, time_var)
    
    def send_restart(self):
        if self.serial_connection:
            try:
                data_to_send = "Start...\n\r\n"
                self.serial_connection.write(data_to_send.encode('utf-8'))
            except (serial.SerialException, OSError) as e:
                self.data_text.insert(tk.END, f"Error sending restart command: {e}\n")
                self.data_text.see(tk.END)

    def save_config(self):
        config = {
            "port": self.port_var.get(),
            "engines": [(step_var.get(), period_var.get(), time_var.get()) for step_var, period_var, time_var in self.engines_info]
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f)
    
    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {}
    
    def load_previous_config(self):
        if self.config:
            self.port_var.set(self.config.get("port", ""))
            engines_config = self.config.get("engines", [])
            for (step_var, period_var, time_var), engine_config in zip(self.engines_info, engines_config):
                if len(engine_config) == 3:
                    step_var.set(engine_config[0])
                    period_var.set(engine_config[1])
                    time_var.set(engine_config[2])
            self.connect_to_port()
    
    def clear_config(self):
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
        self.load_config()
        for step_var, period_var, time_var in self.engines_info:
            step_var.set(0)
            period_var.set(0)
            time_var.set(0)
        self.data_text.insert(tk.END, "Configuration cleared.\n")
        self.data_text.see(tk.END)
    
    def on_close(self):
        self.stop_reading = True
        if self.serial_connection:
            self.serial_connection.close()
        self.save_config()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SerialApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
