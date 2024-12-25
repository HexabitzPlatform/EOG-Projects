import serial
import struct
import logging
import time
import os
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import tkinter as tk

# Setting up the serial connection with the Hexabitz module
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=921600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0
)

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EyeSignalProcessor:
    def __init__(self, samples_count=100, threshold=3.2, capture_interval=5):
        """Initialize the processor with sample count, threshold, and capture interval."""
        self.samples_count = samples_count
        self.threshold = threshold
        self.capture_interval = capture_interval
        self.last_capture_time = 0

    def read_eye_signals(self):
        """Reads eye signals from the serial port."""
        signals = []
        for _ in range(self.samples_count):
            try:
                x = ser.read(4) # Read 4 bytes
                if x and len(x) == 4:
                    signal = struct.unpack('f', x)[0]
                    signals.append(signal)
                    logging.info(f"Sensor Value: {signal}")
            except Exception as e:
                logging.warning(f"Failed to read signal: {e}")
        return np.array(signals)

    def check_and_capture(self, signals):
        """Checks if any signal exceeds the threshold and captures an image if the interval has passed."""
        if np.any(signals > self.threshold):
            current_time = time.time()
            if current_time - self.last_capture_time > self.capture_interval:
                self.capture_image()
                self.last_capture_time = current_time

    def capture_image(self):
        """Captures an image using the Raspberry Pi camera."""
        os.system('raspistill -o image.jpg')
        logging.info("Image captured!")
        self.apply_effects()
        self.show_flash()

    def apply_effects(self):
        """Applies effects to the captured image."""
        try:
            image = Image.open('image.jpg')
            # Apply a filter effect
            image = image.filter(ImageFilter.GaussianBlur(2))
            # Enhance color
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(1.5)
            image.save('image_with_effects.jpg')
            logging.info("Effects applied to the image!")
        except Exception as e:
            logging.warning(f"Failed to apply effects: {e}")

    def show_flash(self):
        """Shows a flash effect to indicate image capture using Tkinter."""
        def close_flash():
            flash.destroy()

        flash = tk.Tk()
        flash.overrideredirect(1)
        flash.geometry("300x200+500+300")  # You can adjust the size and position of the flash window
        flash.config(bg='white')
        flash.after(100, close_flash)  # Flash duration in milliseconds
        flash.mainloop()
        logging.info("Flash effect displayed!")

def main():
    """Main program loop."""
    processor = EyeSignalProcessor()
    while True:
        signals = processor.read_eye_signals()
        processor.check_and_capture(signals)
        time.sleep(0.1) # Short wait before the next loop iteration to avoid consuming too many resources

if __name__ == "__main__":
    main()
