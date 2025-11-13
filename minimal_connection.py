#!/usr/bin/env python3

import asyncio
import xml.etree.ElementTree as ET
import pytak

from configparser import ConfigParser



def gen_cot():
    """Generate minimal CoT Event."""
    root = ET.Element("event")
    root.set("version", "2.0")
    root.set("type", "a-f-G-E-V-C")  # minimal type of marker
    root.set("uid", "minimal_marker")
    root.set("how", "h-g-i-g-o")  # minimal 'how' value
    root.set("time", pytak.cot_time())
    root.set("start", pytak.cot_time())
    root.set("stale", pytak.cot_time(60))  # 60 seconds stale time

    ET.SubElement(root, "point", attrib={"lat": "0.0", "lon": "0.0", "hae": "0", "ce": "9999999", "le": "9999999"})

    return ET.tostring(root)


class MySender(pytak.QueueWorker):
    """
    Defines how you process or generate your Cursor-On-Target Events.
    From there it adds the COT Events to a queue for TX to a COT_URL.
    """

    async def handle_data(self, data):
        """Handle pre-CoT data, serialize to CoT Event, then puts on queue."""
        event = data
        await self.put_queue(event)

    async def run(self):
        """Run the loop for processing or generating pre-CoT data."""
        while True:
            data = gen_cot()
            self._logger.info("Sending:\n%s\n", data.decode())
            await self.handle_data(data)
            await asyncio.sleep(5)


class MyReceiver(pytak.QueueWorker):
    """Defines how you will handle events from RX Queue."""

    async def handle_data(self, data):
        """Handle data from the receive queue."""
        self._logger.info("Received:\n%s\n", data.decode())

    async def run(self):
        """Read from the receive queue, put data onto handler."""
        while True:
            data = (
                await self.queue.get()
            )  # this is how we get the received CoT from rx_queue
            await self.handle_data(data)


async def main():
    """Main definition of your program, sets config params and
    adds your serializer to the asyncio task list.
    """
    config = ConfigParser()

    config["mycottool"] = {"COT_URL": "tcp://172.20.10.6:8088",
                        #    "PYTAK_TLS_CLIENT_CERT": "/home/pi/TAK_RFID_Reader/pytak-eud.pem",
                        #    "PYTAK_TLS_DONT_VERIFY": "1",
                        #    "PYTAK_TLS_CLIENT_CAFILE": "/home/pi/TAK_RFID_Reader/pytak-ca.pem",
                           }
    config = config["mycottool"]

    # Initializes worker queues and tasks.
    clitool = pytak.CLITool(config)
    await clitool.setup()

    # Add your serializer to the asyncio task list.
    clitool.add_tasks(
        set([MySender(clitool.tx_queue, config), MyReceiver(clitool.rx_queue, config)])
    )

    # Start all tasks.
    await clitool.run()


if __name__ == "__main__":
    asyncio.run(main())