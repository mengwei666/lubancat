import serial
import time
import threading

def read_from_serial(port, baudrate=115200, timeout=1):
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        while True:
            time.sleep(1)
            if ser.in_waiting > 0:
                read_result = ser.read(ser.in_waiting).decode('utf-8')
                print(f"Read from {port}: {read_result}")
            else:
                print(f"No data available from {port}")
    except Exception as e:
        print(f"Error reading from {port}: {e}")
    finally:
        ser.close()

def write_to_serial(port, message, baudrate=115200):
    try:
        ser = serial.Serial(port, baudrate)
        while True:
            time.sleep(1)
            ser.write(message.encode('utf-8'))
            print(f"Successfully wrote to {port}")
    except Exception as e:
        print(f"Error writing to {port}: {e}")
    finally:
        ser.close()

if __name__ == "__main__":
    read_port = '/dev/ttyS7'
    write_port = '/dev/ttyS7'
    write_message = "I'm lubancat"

    read_thread = threading.Thread(target=read_from_serial, args=(read_port,))
    write_thread = threading.Thread(target=write_to_serial, args=(write_port, write_message))

    read_thread.start()
    write_thread.start()

    read_thread.join()
    write_thread.join()
