import asyncio
import os
import pytak
from pytak.functions import create_cot_xml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Example of creating a simple CoT Event (a "takPong" to verify connection)
def create_ping_cot():
    """Generates a simple Cursor-on-Target ping event."""
    return create_cot_xml(
        uid="pytak-client-ping",
        type="a-u-pytak-ping",
        latitude=28.1234,  # Replace with actual coordinates
        longitude=-82.5678,
        stale=60,  # CoT event is valid for 60 seconds
        how="h-g-i-l-o"
    )

async def main():
    """
    Runs the PyTAK client to send a CoT event.
    """
    # Load configuration from environment variables (loaded by dotenv)
    config = pytak.read_config()
    
    # Create an event queue for outgoing CoT messages
    tx_queue = asyncio.Queue()

    # Create a PyTAK client (uses the config automatically)
    client = pytak.TAKClient(config, tx_queue)

    # Put a sample CoT event onto the transmit queue
    cot_event = create_ping_cot()
    await tx_queue.put(cot_event)
    print(f"Queued CoT event: {cot_event.get('uid')}")

    # Start the client tasks (sender, receiver, etc.)
    await client.start()

    # Wait for the queue to empty and tasks to finish
    await tx_queue.join()
    print("CoT event sent. Exiting.")

    # Stop the client after the queue is empty
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
