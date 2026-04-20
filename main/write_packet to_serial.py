import serial
import time

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1)

def send_motor_control_packet(data):
    time.sleep(2)
    message = bytes(data + '\n', 'utf-8')
    arduino.write(message)
    print(f"{data}")

if __name__ == "__main__":
        send_motor_control_packet("25 | 0")