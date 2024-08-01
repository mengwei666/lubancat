import serial
import time
import threading
import binascii

def read_from_serial(port, baudrate=115200, timeout=1):
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        while True:
            time.sleep(1)
            if ser.in_waiting > 0:
                # 读取所有待处理的数据并以十六进制字符串形式输出
                read_result = ser.read(ser.in_waiting)
                hex_data = read_result.hex()  # 转换为十六进制字符串
                print(f"Read from {port}: {hex_data}") # 输出为十六进制字符串
                                # 检查数据长度是否足够
                if len(hex_data) >= 16:  # 数据长度应至少为 16 个字符（8 字节）
                    # 获取第八位的值（从0开始索引，第16-17个字符）
                    eighth_byte = hex_data[14:16]
                    print(f"Value of the eighth byte: {eighth_byte}")
            
            
            else:
                print(f"No data available from {port}")
    except Exception as e:
        print(f"Error reading from {port}: {e}")
    finally:
        ser.close()

def write_to_serial(port, message_hex, baudrate=115200):
    try:
        ser = serial.Serial(port, baudrate)
        while True:
            time.sleep(1)
            # 将十六进制字符串转换为字节数据并发送
            message_bytes = binascii.unhexlify(message_hex.replace(" ", ""))
            ser.write(message_bytes)
            print(f"Successfully wrote to {port}")
    except Exception as e:
        print(f"Error writing to {port}: {e}")
    finally:
        ser.close()

if __name__ == "__main__":
    read_port = '/dev/ttyS7'
    write_port = '/dev/ttyS7'
    write_message_hex = "050AFFAA3197040100F461"  # 十六进制字符串（去除空格）

    read_thread = threading.Thread(target=read_from_serial, args=(read_port,))
    write_thread = threading.Thread(target=write_to_serial, args=(write_port, write_message_hex))

    read_thread.start()
    write_thread.start()

    read_thread.join()
    write_thread.join()
