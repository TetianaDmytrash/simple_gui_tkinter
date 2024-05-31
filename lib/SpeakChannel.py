import threading
import time

import serial


class SpeakCOMPort:
    def __init__(self, port_var, step_period_var, response_frame):
        self.port_var = port_var
        self.step_period_var = step_period_var
        self.response_frame = response_frame
        self._serial_connect = None

    def open_channel(self):
        print(f"start open connect with port")
        selected_port = self.port_var.get_port()
        if selected_port:
            print(f"#Opening port: {selected_port}")
            self.response_frame.write_response(f"#Opening port: {selected_port}")
            try:
                self._serial_connect = serial.Serial(selected_port, baudrate=115200, timeout=1)
                self.response_frame.write_response(f"Port {selected_port} opened successfully.")
                self.send_request()
            except Exception as e:
                print(f"error occurred during open connection with COM port: {e}")
                self.response_frame.write_response(f"error occurred during open connection with COM port: {e}")
        else:
            print("No port selected.")
            self.response_frame.write_response("No port selected.")

    def send_request(self):
        """
        engine[0] - engine number
        engine[1] - steps
        engine[2] - period
        :return:
        """
        print(f"step and period information: {self.step_period_var.get_step_period_info()}")
        for engine in self.step_period_var.get_step_period_info():
            request_string = f"set:{engine[0]};{engine[1]};{engine[2]}."
            self.response_frame.write_response(f"->send data: {request_string}")
            if self._serial_connect and self._serial_connect.is_open:
                self._serial_connect.write(request_string.encode())
                print(f"send data: {request_string}")
                self.response_frame.write_response(f"->send data: {request_string}")
            else:
                print("#port is not open.")
                self.response_frame.write_response("#port is not open.")

    def start_reading(self):
        if not self.reading:
            self.reading = True
            self.read_thread = threading.Thread(target=self.read_from_port)
            self.read_thread.start()

    def read_from_port(self):
        while self.reading:
            if self._serial_connect.in_waiting > 0:
                data = self._serial_connect.readline().decode('utf-8').strip()
                print(f"Received: {data}")
            time.sleep(0.1)  # Sleep briefly to prevent high CPU usage

    def stop_reading(self):
        self.reading = False
        if self.read_thread is not None:
            self.read_thread.join()

    def close_channel(self):
        self.stop_reading()
        if self._serial_connect.is_open:
            self._serial_connect.close()
            print(f"Closed channel on port {self._serial_connect.port}")
