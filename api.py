import requests
s = requests.session()
address = "http://45.55.177.62:8080"
r = s.get(f"{address}/api/login", json={}, verify=False)
csrf_token = r.json()['response']['csrf_token']
s.headers['X-XSRF-TOKEN'] = csrf_token
s.headers['Referer'] = address

r = s.post(f"{address}/api/login", json={'username': 'test', 'password': 'test'}, verify=False)
r = s.post(f"{address}/api/markers", json={'latitude': '29.647074', 'longitude': '-82.347934', 'name': 'marker0', 'uid': '00000000-0000-4000-8000-000000000000'}, verify=False)
print(r.text)