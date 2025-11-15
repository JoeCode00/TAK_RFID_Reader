#!/usr/bin/env python3
"""
Simple PyTAK client that talks to an OpenTAKServer over plain TCP
( non‑TLS ) on port 5000.

It sends a periodic "heartbeat" CoT XML message that shows up on the
dashboard as a moving point.  The code follows the examples in the
pytak repository (https://github.com/snstac/pytak).

Author:  (you can put your name here)
"""

import argparse
import time
import uuid
import sys
from datetime import datetime, timezone, timedelta

# Import the core PyTAK classes
from pytak import TakMessage, TcpClient

# ----------------------------------------------------------------------
# Helper: generate a minimal CoT (Cursor‑on‑Target) XML payload
# ----------------------------------------------------------------------


def build_heartbeat_xml(uid: str, lat: float, lon: float, alt: float = 0.0) -> str:
    """
    Return a string containing a CoT “heartbeat” XML document.

    The fields we need:
      * uid          – unique identifier for this device (e.g. callsign)
      * lat, lon, alt – position (alt in meters, optional)
      * time         – current UTC timestamp in ISO‑8601 format
      * start        – same as time (when the event started)
      * stale        – when the event should be considered stale (now+5m)

    The structure is based on the official CoT schema used by TAK.
    """
    now = datetime.now(timezone.utc)
    time_str = now.isoformat(timespec='seconds')
    stale_str = (now + timedelta(minutes=5)).isoformat(timespec='seconds')

    # Minimal set of XML attributes – you can add more (detail, remarks, etc.)
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<event version="2.0" uid="{uid}"
       type="a-f-G-U-C"
       time="{time_str}"
       start="{time_str}"
       stale="{stale_str}"
       how="m-g">
  <point lat="{lat:.6f}" lon="{lon:.6f}" hae="{alt:.1f}" ce="9999999" le="9999999"/>
  <detail>
    <contact callsign="{uid}"/>
    <precisionlocation geopointsrc="GPS"/>
  </detail>
</event>"""
    return xml

# ----------------------------------------------------------------------
# Main client logic
# ----------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="PyTAK plain‑TCP client for OpenTAKServer"
    )
    parser.add_argument(
        "--host", default="45.55.177.62",
        help="IP address or hostname of the OpenTAKServer (default: %(default)s)"
    )
    parser.add_argument(
        "--port", type=int, default=5000,
        help="TCP port the server listens on for plain CoT (default: %(default)s)"
    )
    parser.add_argument(
        "--callsign", default="RPI4",
        help="Unique identifier for this device (default: %(default)s)"
    )
    parser.add_argument(
        "--lat", type=float, default=28.6024,
        help="Initial latitude (default: %(default)s)"
    )
    parser.add_argument(
        "--lon", type=float, default=-81.2001,
        help="Initial longitude (default: %(default)s)"
    )
    parser.add_argument(
        "--interval", type=int, default=10,
        help="Seconds between heartbeat messages (default: %(default)s)"
    )
    args = parser.parse_args()

    # Build a stable UID – we use a UUID plus the callsign to guarantee uniqueness
    uid = f"{args.callsign}-{uuid.uuid4()}"

    # ------------------------------------------------------------------
    # Set up the TCP client (plain, no TLS)
    # ------------------------------------------------------------------
    client = TcpClient(host=args.host, port=args.port, ssl=False)

    print(f"Connecting to {args.host}:{args.port} …")
    try:
        client.connect()
    except Exception as exc:
        print(f"❌  Could not connect: {exc}")
        sys.exit(1)

    print("✅  Connected – sending heartbeats every"
          f" {args.interval} seconds. Ctrl‑C to stop.\n")

    # ------------------------------------------------------------------
    # Main loop: generate a heartbeat, wrap it in a TakMessage, send it
    # ------------------------------------------------------------------
    try:
        while True:
            # (Optional) you could move the lat/lon slightly each iteration
            # to simulate motion; for now we keep them constant.
            xml_payload = build_heartbeat_xml(uid, args.lat, args.lon)

            # Convert the XML string to a TakMessage (the library knows the
            # required binary framing for TCP).
            msg = TakMessage(xml_payload.encode('utf-8'))

            # Send the message over the already‑opened socket
            client.send(msg)

            print(f"[{datetime.now().strftime('%H:%M:%S')}] Sent heartbeat")
            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\n👋  Stopping – closing connection")
    finally:
        client.close()


if __name__ == "__main__":
    main()
