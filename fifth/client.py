import asyncio
from websockets import connect


async def hello(uri):
    async with connect(uri) as websocket:
        await websocket.send("Hello world!")
        data = await websocket.recv()
        print(data)

asyncio.run(hello("ws://localhost:8000/cities/biggest"))
