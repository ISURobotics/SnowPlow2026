import serial
import threads
import threaded
import time
import sys

SERIAL_PORTS = [
    {"port": "/dev/ttyCH341USB1", "baudrate": 115200, "name": "Controller"},
    {"port": "/dev/ttyCH341USB0", "baudrate": 115200, "name": "Gyro"},
    {"port": "/dev/ttyACM0", "baudrate": 115200, "name": "GPS"}
]
OUTPUT_FILE = "log.txt"

def read_from_port(port_config):
    port_name = port_config["port"]
    baud_rate = port_config["baudrate"]
    device_name = port_config["name"]

    try:
        ser = serial.Serial(port_name, baud_rate, timeout=1)
        print(f"Opened {device_name} on {port_name}")

        while True:

            line = ser.readline().decode('latin-1').strip()

            if line:
                log_entry = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {device_name}: {line}\n"
                log_entry = (f"{device_name}: {line}")
                print(log_entry)
                if 'Controller: ' in log_entry:
                    controller_data = str(log_entry.rsplit(': ')[1])
                    print(controller_data)

                if 'Gyro: Orient: ' in log_entry:
                    imu_orient_data = str(log_entry.rsplit(': ')[1])
                    print(imu_orient_data)

                if 'Gyro: Gyro: ' in log_entry:
                    imu_gyro_data = str(log_entry.rsplit('Gyro: Gyro: ')[1])
                    print(imu_gyro_data)

                if 'Gyro: Linear: ' in log_entry:
                    imu_linear_data = str(log_entry.rsplit('Gyro: Linear: ')[1])
                    print(imu_linear_data)

                if 'Gyro: Mag: ' in log_entry:
                    imu_mag_data = str(log_entry.rsplit('Gyro: Mag: ')[1])
                    print(imu_mag_data)

                if 'Gyro: Accl: ' in log_entry:
                    imu_accl_data = str(log_entry.rsplit('Gyro: Accl: ')[1])
                    print(imu_accl_data)

                if 'Gyro: Gravity: ' in log_entry:
                    imu_gravity_data = str(log_entry.rsplit('Gyro: Gravity: ')[1])
                    print(imu_gravity_data)

                if 'Gyro: Temperature: ' in log_entry:
                    imu_temperature_data = str(log_entry.rsplit('Gyro: Temperature: ')[1])
                    print(imu_temperature_data)

                if 'Gyro: Calibration: ' in log_entry:
                    imu_calibration_data = str(log_entry.rsplit('Gyro: Calibration: ')[1])
                    print(imu_calibration_data)

                if 'GPS: $GNRMC' in log_entry:
                    gps_gnrmc_data = str(log_entry.rsplit('GPS: $GNRMC')[1])
                    print(gps_gnrmc_data)

                if 'GPS: $GNVTG' in log_entry:
                    gps_gnvtg_data = str(log_entry.rsplit('GPS: $GNVTG')[1])
                    print(gps_gnvtg_data)

                if 'GPS: $GNGGA' in log_entry:
                    gps_gngga_data = str(log_entry.rsplit('GPS: $GNGGA')[1])
                    print(gps_gngga_data)

                if 'GPS: $GNGSA' in log_entry:
                    gps_gngsa_data = str(log_entry.rsplit('GPS: $GNGSA')[1])
                    print(gps_gngsa_data)

    except serial.SerialException as e:
        print(f"Error opening/reading from {port_name}: {e}")
        ser.close()

    except KeyboardInterrupt:
        print(f"Stopping read from {port_name}.")
        ser.close()

    finally:
        if 'ser' in locals() and ser.isOpen():
            ser.close()

if __name__ == "__main__":
    threads = []

    for config in SERIAL_PORTS:
        thread = threading.Thread(target=read_from_port, args=(config,))
        thread.daemon = True  # Allows the main program to exit even if threads are running
        threads.append(thread)
        thread.start()

    print(f"Logging to {OUTPUT_FILE}.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Main program received KeyboardInterrupt, exiting.")
        sys.exit(0)
