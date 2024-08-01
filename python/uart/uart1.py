import serial
import time
import threading
import tkinter as tk
from tkinter import scrolledtext

def read_from_serial(port, baudrate=115200, timeout=1, text_widget=None):
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        while True:
            time.sleep(1)
            if ser.in_waiting > 0:
                read_result = ser.read(ser.in_waiting).decode('utf-8')
                if text_widget:
                    text_widget.insert(tk.END, f"Read from {port}: {read_result}\n")
                    text_widget.see(tk.END)
            else:
                if text_widget:
                    text_widget.insert(tk.END, f"No data available from {port}\n")
                    text_widget.see(tk.END)
    except Exception as e:
        if text_widget:
            text_widget.insert(tk.END, f"Error reading from {port}: {e}\n")
            text_widget.see(tk.END)
    finally:
        ser.close()

def write_to_serial(port, message, baudrate=115200, text_widget=None):
    try:
        ser = serial.Serial(port, baudrate)
        while True:
            time.sleep(1)
            ser.write(message.encode('utf-8'))
            if text_widget:
                text_widget.insert(tk.END, f"Sent to {port}: {message}\n")
                text_widget.see(tk.END)
    except Exception as e:
        if text_widget:
            text_widget.insert(tk.END, f"Error writing to {port}: {e}\n")
            text_widget.see(tk.END)
    finally:
        ser.close()

def start_serial_threads(read_port, write_port, write_message, text_widget):
    read_thread = threading.Thread(target=read_from_serial, args=(read_port, 115200, 1, text_widget))
    write_thread = threading.Thread(target=write_to_serial, args=(write_port, write_message, 115200, text_widget))

    read_thread.start()
    write_thread.start()

def create_gui():
    root = tk.Tk()
    root.title("Serial Port Communication")

    text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
    text_widget.pack(padx=10, pady=10)

    start_button = tk.Button(root, text="Start Communication", 
                             command=lambda: start_serial_threads('/dev/ttyS7', '/dev/ttyS7', "I'm lubancat", text_widget))
    start_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
