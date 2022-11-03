import time
import asyncio


async def main():
    print("Running...")

    while True:
        from main import manager
        await manager.broadcast("Hello world")
        print("Sent message, sleeping 5...")
        print("Active conections: ", manager.active_connections)
        time.sleep(5)

if __name__ == '__main__':
    asyncio.run(main())
