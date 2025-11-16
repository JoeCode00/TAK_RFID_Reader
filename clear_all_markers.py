import requests
s = requests.session()
address = "http://45.55.177.62:8080"
r = s.get(f"{address}/api/login", json={}, verify=False)
csrf_token = r.json()['response']['csrf_token']
s.headers['X-XSRF-TOKEN'] = csrf_token
s.headers['Referer'] = address

r = s.post(f"{address}/api/login", json={'username': 'administrator', 'password': 'password'}, verify=False)
response_markers = s.get(f"{address}/api/markers", json={}, verify=False)
for marker in response_markers.json()['results']:
    uid = marker['uid']
    print(f"Deleting marker with UID: {uid}")
    response_delete = s.delete(f"{address}/api/markers", params={'uid': uid}, verify=False)
    print(f"Response: {response_delete.status_code} - {response_delete.text}")
