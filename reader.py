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
    timeout=0.2  # Read timeout in seconds
)

try:
    # Open the serial port
    try:
        ser.open()
    except Exception as e:
        False
    while True:
        ser.write(bytes([0x0A, 0x55, 0x30, 0x2C, 0x52, 0x31, 0x2C, 0x30, 0x2C, 0x31, 0x0D]))

        received_line = ser.readline()
        string_data = received_line.decode('utf-8').strip()  # Decode bytes to string and strip whitespace
        split = string_data.split(",")
        for item in split:
            if item is not None:
                if len(item)>0:
                    if item[0]=="E":
                        card = item
                        print(card)

        # if ser.in_waiting > 28:
        #     data = ser.read(ser.in_waiting) # Read all available bytes
        #     string_data = data.decode('utf-8').strip()  # Decode bytes to string and strip whitespace
        #     split = string_data.split(",")
        #     for item in split:
        #         if item is not None:
        #             if len(item)>0:
        #                 if item[0]=="E":
        #                     card = item
        #                     print(card)
        time.sleep(0.01)
    # # --- Receiving Bytes ---
    # # Read up to 100 bytes (or until timeout)
    # received_data = ser.read(100)
    # if received_data:
    #     # Decode the received bytes to a string
    #     print(f"Received: {received_data.decode('utf-8')}")
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