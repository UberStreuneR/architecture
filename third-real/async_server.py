from typing import List
import time
import asyncio


class Server:
    def __init__(self):
        self.messages = []
        self.writers: List[asyncio.StreamWriter] = []

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        hello_request = (await reader.read(255)).decode('utf-8')
        if hello_request == "client":
            print("Handling client")
            self.writers.append(writer)
            return
        print("Handling sender")
        start = time.perf_counter()
        while True:
            request = (await reader.read(255)).decode('utf-8')
            now = time.perf_counter()
            self.messages.append(request)
            if now - start > 5:
                await self.spam_messages()

    async def run_server(self):
        server = await asyncio.start_server(self.handle_client, 'localhost', 10000)
        async with server:
            print("Serving forever")
            await server.serve_forever()
            print("Stopped serving")

    async def spam_messages(self):
        print("Writing messages", self.messages)
        for message in self.messages:
            for writer in self.writers:
                writer.write(message.encode("utf-8"))
                await writer.drain()
        self.messages = []


server = Server()
asyncio.run(server.run_server())
asyncio.run(server.spam_messages())
