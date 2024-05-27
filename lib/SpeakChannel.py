import serial


class SpeakCOMPort:
    def __init__(self, port_var):
        self.port_var = port_var

    def open_channel(self):
        print(f"start open connect with port")
        try:
            selected_port = self.port_var.get()
            print(f"Opening channel on port: {selected_port}")
            ser = serial.Serial(selected_port, baudrate=9600)
            print(f"I try: {selected_port}")
        except Exception as e:
            print(f"error occurred during open connection with COM port: {e}")

