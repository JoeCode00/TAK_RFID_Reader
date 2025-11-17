import requests
import RPi.GPIO as GPIO
import time
import atexit

# GPIO setup for button
BUTTON_PIN = 18  # Change this to your desired GPIO pin number
REQUIRE_BUTTON = False

def setup_gpio():
    """Initialize GPIO with proper cleanup"""
    try:
        # Clean up any previous GPIO setup
        GPIO.cleanup()

        # Set GPIO mode and setup button pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Register cleanup function to run on exit
        atexit.register(GPIO.cleanup)

        print(f"GPIO setup complete on pin {BUTTON_PIN}")

    except Exception as e:
        print(f"GPIO setup error: {e}")
        raise


def wait_for_button_press():
    """Wait for button press before continuing"""
    print("Waiting for button press to start marker creation...")

    try:
        # Alternative approach: poll the button state instead of using wait_for_edge
        print("Polling button state (press button or wait 30 seconds)...")
        start_time = time.time()
        button_pressed = False

        while time.time() - start_time < 30:  # 30 second timeout
            # Read current button state (LOW when pressed due to pull-up)
            if GPIO.input(BUTTON_PIN) == GPIO.LOW:
                # Debounce - check if still pressed after short delay
                time.sleep(0.05)
                if GPIO.input(BUTTON_PIN) == GPIO.LOW:
                    button_pressed = True
                    break
            time.sleep(0.1)  # Small delay to prevent excessive CPU usage

        if button_pressed:
            print("Button pressed! Starting marker creation process...")
            # Wait for button release to avoid multiple triggers
            while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                time.sleep(0.05)
        else:
            print("No button press detected within timeout period. Continuing anyway...")

    except Exception as e:
        print(f"Button wait error: {e}")
        print("Continuing with marker creation...")


# Initialize GPIO
setup_gpio()

if REQUIRE_BUTTON:
    wait_for_button_press()

s = requests.session()
address = "http://45.55.177.62:8080"
r = s.get(f"{address}/api/login", json={}, verify=False)
csrf_token = r.json()['response']['csrf_token']
s.headers['X-XSRF-TOKEN'] = csrf_token
s.headers['Referer'] = address

r = s.post(f"{address}/api/login", json={'username': 'marker',
           'password': 'marker'}, verify=False)

markers = [['29.647074', '-82.347934', 'aaaaa'],
           ['29.647111', '-82.347507', 'bbbbb'],
           ['29.647136', '-82.347376', 'ccccc'],
           ['29.647134', '-82.347215', 'ddddd'],
           ['29.647211', '-82.347024', 'eeeee']]

for index, marker in enumerate(markers):
    latitude = marker[0]
    longitude = marker[1]
    name = marker[2]
    uid = '00000000-0000-4000-8000-00000000000' + str(index)
    r = s.post(f"{address}/api/markers", json={'latitude': latitude,
               'longitude': longitude, 'name': name, 'uid': uid, 'relation': 'a'}, verify=False)
    print(f"Response: {r.status_code} - {r.text}")
