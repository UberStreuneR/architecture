from fastapi import FastAPI, WebSocket
import asyncio
from typing import List

app = FastAPI()


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ConnectionManager(metaclass=SingletonMeta):
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.messages: List[str] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def add_message(self, message: str):
        self.messages.append(message)

    async def broadcast_messages(self):
        for message in self.messages[:]:
            await self.broadcast(message)
            self.messages.remove(message)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    manager = ConnectionManager()
    await manager.connect(websocket)
    while True:
        data = await websocket.receive_text()
        print(data)
        await manager.add_message(data)


@app.get("/broadcast")
async def broadcast_endpoint():
    manager = ConnectionManager()
    while True:
        print(manager.active_connections, manager.messages)
        await manager.broadcast_messages()
        # await manager.broadcast("Message")
        await asyncio.sleep(5)
