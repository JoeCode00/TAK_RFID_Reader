import asyncio
import pytak
from configparser import ConfigParser

async def main():
    """
    Connect to FreeTAKServer via TCP and send a basic CoT data package.
    """
    # Create configuration
    config = ConfigParser()
    config.add_section('pytak')
    config.set({'COT_URL':'tcp://172.20.10.6:8087'})
    
    # Create event queues
    tx_queue = asyncio.Queue()
    rx_queue = asyncio.Queue()
    
    # Create a basic CoT event
    cot_event = pytak.gen_cot_xml(
        uid="pytak-test-001",
        cot_type="a-f-G-E-S",  # Ground equipment
        lat=37.7749,
        lon=-122.4194,
        stale=60,
    )
    
    # Queue the event for transmission
    await tx_queue.put(cot_event)
    print(f"Sending CoT event to 172.20.10.6:8087...")
    
    # Create protocol (network connection)
    reader, writer = await pytak.protocol_factory(config)
    
    # Create TX worker to send messages
    tx_worker = pytak.TXWorker(tx_queue, config, writer)
    
    # Run the TX worker to send the event
    done, pending = await asyncio.wait(
        {tx_worker.run()},
        timeout=5.0,
        return_when=asyncio.FIRST_COMPLETED
    )
    
    print("Event sent successfully!")
    
    # Close connection
    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
