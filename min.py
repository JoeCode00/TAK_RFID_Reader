import asyncio
import pytak


async def main():
    """Connect to TAK server over TCP"""
    # Configure the TAK client
    config = pytak.Config()
    config.COT_URL = 'tcp://172.20.10.6:8087'  # TAK server TCP endpoint
    
    # Create event queue
    clitool = pytak.CLITool(config)
    await clitool.setup()
    
    # Create and run the client
    await clitool.run()


if __name__ == '__main__':
    asyncio.run(main())
