import asyncio
from websockets.asyncio.client import connect
# Sample echo websocket client from python websockets documentation

async def hello():
    async with connect("ws://localhost:7777") as websocket:
        await websocket.send("Hello World!")
        message = await websocket.recv()
        print(message)


if __name__ == "__main__":
    asyncio.run(hello())