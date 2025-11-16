import requests
s = requests.session()
address = "http://45.55.177.62:8080"
r = s.get(f"{address}/api/login", json={}, verify=False)
csrf_token = r.json()['response']['csrf_token']
s.headers['X-XSRF-TOKEN'] = csrf_token
s.headers['Referer'] = address

r = s.post(f"{address}/api/login", json={'username': 'reader', 'password': 'reader'}, verify=False)
response_markers = s.get(f"{address}/api/markers", json={}, verify=False)
for marker in response_markers.json()['results']:
    callsign = marker['callsign']
    lattitude = marker['point']['latitude']
    longitude = marker['point']['longitude']
    print(callsign, lattitude, longitude)

import serial
import time
# Configure the serial port
# Replace 'COM1' with your actual serial port (e.g., '/dev/ttyUSB0' on Linux)
# Set the baudrate to match your device's configuration
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=38400,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=0  # Read timeout in seconds
)

try:
    # Open the serial port
    try:
        ser.open()
    except Exception as e:
        False
    while True:
        time.sleep(0.05)
        ser.write(bytes([0x0A, 0x55, 0x30, 0x2C, 0x52, 0x31, 0x2C, 0x30, 0x2C, 0x31, 0x0D]))

        data = ser.readall()
        data.replace(b'\r\r', b'').replace(b'\n\n', b'')
        cleaned = data.replace(b'\nU\r\n', b'').replace(b'\nX\r\n', b'')
        if cleaned not in [b'', b'\r', b'\n', b'U', b'X', b'\r\n', b'\nU', b'\nX', b'U\r\n', b'X\r\n', b'X\r', b'U\r', b'\nU\r', b'\nX\r']:
            print(cleaned.decode('utf-8').strip())
        
        # # --- Receiving Bytes ---
        # # Read up to 100 bytes (or until timeout)
        # if ser.in_waiting >= 39:
        #     time.sleep(0.2)  # Wait a bit for all data to arrive

        #     received_data = ser.read(80)
        #     decode = received_data.decode('utf-8').strip()
        #     if decode[1] != '\r':
        #         # Decode the received bytes to a string
        #         print(received_data)
        # else:
        #     print("No data received within the timeout period.")

        # You can also use readline() to read until a newline character
        # received_line = ser.readline()
        # if received_line:
        #     print(f"Received line: {received_line.decode('utf-8').strip()}")

except serial.SerialException as e:
    print(f"Error: {e}")

finally:
    # Close the serial port when done
    if ser.is_open:
        ser.close()
        print(f"Serial port {ser.port} closed.")