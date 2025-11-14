import asyncio
import pytak


async def main():
    """Connect to TAK server over TCP"""
    # Configure the TAK client
    config = {
        'COT_URL': 'tcp://172.20.10.6:8087',  # TAK server TCP endpoint
    }
    
    # Create a TAK client
    client = pytak.TXWorker(
        # event_queue=asyncio.Queue(),
        url=config['COT_URL']
    )
    
    try:
        await client.run()
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        await client.stop()


if __name__ == '__main__':
    asyncio.run(main())
