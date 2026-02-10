from serial import Serial
from pyubx2 import UBXReader

serial_port = "/dev/ttyACM0"
baud_rate = 115200

try:
    with Serial(serial_port, baud_rate, timeout=3) as stream:
        ubr = UBXReader(stream)

        for raw_data, parsed_data in ubr:
            if hasattr(parsed_data, "lat") and hasattr(parsed_data, "lon"):
                storedLongitude = (f"Latitude: {parsed_data.lat}")
                storedLatitude= (f"Longitude: {parsed_data.lon}")
                print(storedLongitude)
                print(storedLatitude)
            else:
                stored = (f"Received message: {parsed_data.identity}")

except Exception as e:
    print(f"Error: {e}")