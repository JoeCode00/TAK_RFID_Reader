import requests
import RPi.GPIO as GPIO
import time

# GPIO setup for button
BUTTON_PIN = 18  # Change this to your desired GPIO pin number
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def wait_for_button_press():
    """Wait for button press before continuing"""
    print("Waiting for button press to start marker creation...")

    # Wait for button press (falling edge - button pressed)
    GPIO.wait_for_edge(BUTTON_PIN, GPIO.FALLING)

    # Debounce delay
    time.sleep(0.2)

    print("Button pressed! Starting marker creation process...")


wait_for_button_press()

s = requests.session()
address = "http://45.55.177.62:8080"
r = s.get(f"{address}/api/login", json={}, verify=False)
csrf_token = r.json()['response']['csrf_token']
s.headers['X-XSRF-TOKEN'] = csrf_token
s.headers['Referer'] = address

r = s.post(f"{address}/api/login", json={'username': 'marker',
           'password': 'marker'}, verify=False)

markers = [['29.647074', '-82.347934'],
           ['29.647111', '-82.347507'],
           ['29.647136', '-82.347376'],
           ['29.647134', '-82.347215'],
           ['29.647211', '-82.347024']]

for index, marker in enumerate(markers):
    latitude = marker[0]
    longitude = marker[1]
    name = str(index)
    uid = '00000000-0000-4000-8000-00000000000' + str(index)
    r = s.post(f"{address}/api/markers", json={'latitude': latitude,
               'longitude': longitude, 'name': name, 'uid': uid}, verify=False)
    print(f"Response: {r.status_code} - {r.text}")
