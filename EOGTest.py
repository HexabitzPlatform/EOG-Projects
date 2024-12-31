import serial
import struct
import time
import numpy as np
import tkinter as tk
from tkinter import font

# Setting up the serial connection with the Hexabitz module
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=115200,  # Try increasing baudrate
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.1  # Reduced timeout for faster reading
)

class EyeSignalProcessor:
    def __init__(self, samples_count=20, threshold=1.2):  # Reduced sample count
        """Initialize the processor with sample count and threshold."""
        self.samples_count = samples_count
        self.threshold = threshold
        self.signals = np.zeros(samples_count)

    def read_eye_signals(self):
        """Reads eye signals from the serial port."""
        for i in range(self.samples_count):
            try:
                x = ser.read(4)  # Read 4 bytes
                if x and len(x) == 4:
                    signal = struct.unpack('f', x)[0]
                    self.signals[i] = signal
            except Exception as e:
                print(f"Failed to read signal: {e}")
        return self.signals

    def determine_light_environment(self):
        """Determines if the environment is dark or light based on threshold."""
        average_signal = np.mean(self.signals)
        if average_signal < self.threshold:
            return "light"
        else:
            return "dark"

def check_environment(processor, label):
    """Check the light environment and update the label."""
    signals = processor.read_eye_signals()
    environment = processor.determine_light_environment()
    if environment == "light":
        label.config(text="DayTime ☀️", bg="#FFD700", fg="black")
    else:
        label.config(text="NightTime :)", bg="#1E90FF", fg="white")

def close_app(root):
    """Close the tkinter application."""
    root.destroy()

def main():
    """Main program loop with tkinter for GUI."""
    processor = EyeSignalProcessor(samples_count=20)  # Reduced sample count for faster updates
    
    # Set up tkinter GUI
    root = tk.Tk()
    root.title("Light and Dark Detector")
    
    # Custom font for labels
    custom_font = font.Font(family="Helvetica", size=24, weight="bold")
    
    check_button = tk.Button(root, text="Check Light Environment", command=lambda: check_environment(processor, result_label), font=custom_font)
    check_button.pack(pady=20)
    
    exit_button = tk.Button(root, text="Exit", command=lambda: close_app(root), font=custom_font)
    exit_button.pack(pady=10)
    
    result_label = tk.Label(root, text="Environment will be shown here", bg="white", fg="black", width=30, height=5, font=custom_font)
    result_label.pack(pady=20)
    
    root.geometry("400x300")  # Adjust window size
    root.configure(bg="#F0F8FF")  # Set background color
    
    root.mainloop()

if __name__ == "__main__":
    main()
