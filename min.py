import asyncio
import configparser
import pytak


async def main():
    """Connect to TAK server over TCP"""
    # Configure the TAK client
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'COT_URL': 'tcp://172.20.10.6:8087'
    }
    
    # Create event queue and workers
    tx_queue = asyncio.Queue()
    rx_queue = asyncio.Queue()
    
    clitool = pytak.CLITool(config, tx_queue, rx_queue)
    await clitool.setup()
    
    # Create and run the client
    await clitool.run()


if __name__ == '__main__':
    asyncio.run(main())
