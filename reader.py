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