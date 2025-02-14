import serial
import time

class SerialConnection:
    _instance = None  # Singleton instance

    def __new__(cls, port="COM3", baudrate=4800, timeout=1):
        if cls._instance is None:
            cls._instance = super(SerialConnection, cls).__new__(cls)
            cls._instance.initialize(port, baudrate, timeout)
        return cls._instance

    def initialize(self, port, baudrate, timeout):
        self.ser = None
        retries = 3
        while retries > 0:
            try:
                self.ser = serial.Serial(port, baudrate, timeout=timeout)
                time.sleep(2)  # Allow Arduino time to stabilize
                print("Connected to Arduino.")
                break
            except serial.SerialException as e:
                print(f"Serial error: {e}")
                retries -= 1
                time.sleep(2)
            except PermissionError as e:
                print(f"Permission error: {e} - Ensure no other process is using {port}")
                break  # Stop retrying if it's a permission issue

    def read_lines(self, num_lines=3):
        if not self.ser:
            return {"error": "No serial connection."}

        data = []
        for _ in range(num_lines):
            try:
                line = self.ser.readline().decode("utf-8").strip()
                if line:
                    data.append(line)
            except serial.SerialException as e:
                print(f"Error reading serial data: {e}")

        return data
