import asyncio
import websockets

# Initialize set of connections
CONNECTIONS = set()

async def securechat(websocket):
    # Add clients to set of connections
    if websocket not in CONNECTIONS:
        CONNECTIONS.add(websocket)
    # Broadcast messages to all clients
    async for message in websocket:
        websockets.broadcast(CONNECTIONS,message)


async def main():
    # Serve websocket server forever
    async with websockets.serve(securechat, "localhost", 7777) as server:
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())