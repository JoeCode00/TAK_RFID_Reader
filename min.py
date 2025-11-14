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
    config.set('pytak', 'COT_URL', 'tcp://172.20.10.6:8087')
    
    # Create event queue for outgoing messages
    tx_queue = asyncio.Queue()
    
    # Create TAK client
    client = pytak.TAKClient(config, tx_queue)
    
    # Create a basic CoT event
    cot_event = pytak.functions.create_cot_xml(
        uid="pytak-test-001",
        type="a-f-G-E-S",  # Ground equipment
        latitude=37.7749,
        longitude=-122.4194,
        stale=60,
        how="h-e"
    )
    
    # Queue the event for transmission
    await tx_queue.put(cot_event)
    print(f"Sending CoT event to 172.20.10.6:8087...")
    print(f"UID: {cot_event.get('uid')}")
    
    # Start client and send
    await client.start()
    await tx_queue.join()
    
    print("Event sent successfully!")
    
    # Stop the client
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
