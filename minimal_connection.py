from pyTAK import Client
from pyTAK.cot import Event, Point, Detail

client = Client(host="172.20.10.6", port=8087, callsign="PYTAK_USER")
client.connect()

event = Event(
    uid="PYTAK-001",
    type="a-u-V",
    time="2025-11-13T10:15:00Z",
    start="2025-11-13T10:15:00Z",
    stale="2025-11-13T10:45:00Z",
    point=Point(lat=29.6516, lon=-82.3248, hae=10),
    detail=Detail(
        contact=dict(callsign="PYTAK_USER"),
        precisionlocation=dict(geopointsrc="GPS", altsrc="Barometric"),
        track=dict(speed=12.3, course=85.0)
    )
)

client.send_coa(event)   # transmit the CoT XML to the OpenTAK server
client.run_forever()
