import asyncio
from websockets.asyncio.server import serve
# Sample echo websocket server from python websockets documentation

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)


async def main():
    async with serve(echo, "localhost", 7777) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())