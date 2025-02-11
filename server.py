import asyncio
import websockets
import json
import hashlib
import secrets
import ssl
import time
from collections import defaultdict

# Temporary user credential storage (hashed passwords)
USERS = {
    "steve": hashlib.sha256("password".encode()).hexdigest(),
    "john": hashlib.sha256("password".encode()).hexdigest(),
}

# Store active connections and user sessions
CONNECTIONS = set()
SESSIONS = {}

# Track message timestamps for rate limiting
RATE_LIMIT = defaultdict(list)

# Rate limit configuration
MAX_MESSAGES = 5  # Maximum messages allowed in time window
MESSAGE_WINDOW = 10  # Time window in seconds


async def securechat(websocket):
    """
    Manages authentication and chat messaging in a secure WebSocket connection.
    - Authenticates users and establishes session tokens.
    - Enforces rate limiting on messages to prevent spam.
    - Broadcasts messages from authenticated users.
    - Handles user disconnects securely.
    """
    try:
        async for message in websocket:
            data = json.loads(message)

            # User login authentication
            if data["type"] == "login":
                username = data["username"]
                password = hashlib.sha256(data["password"].encode()).hexdigest()

                # Verify credentials and assign session token
                if username in USERS and USERS[username] == password:
                    session_token = secrets.token_hex(16)
                    SESSIONS[session_token] = username
                    await websocket.send(json.dumps({"type": "login_success", "token": session_token}))
                else:
                    await websocket.send(json.dumps({"type": "login_failed"}))

            # Handle message broadcasting with rate limiting
            elif data["type"] == "message":
                token = data.get("token")

                # Check if the user is authenticated
                if token in SESSIONS:
                    sender = SESSIONS[token]
                    
                    # Rate limit check
                    now = time.time()
                    RATE_LIMIT[sender] = [t for t in RATE_LIMIT[sender] if now - t < MESSAGE_WINDOW]

                    if len(RATE_LIMIT[sender]) < MAX_MESSAGES:
                        RATE_LIMIT[sender].append(now)  # Store message timestamp

                        if websocket not in CONNECTIONS:
                            CONNECTIONS.add(websocket)

                        full_message = f"{sender}: {data['message']}"
                        websockets.broadcast(CONNECTIONS, json.dumps({"type": "message", "content": full_message}))
                    else:
                        await websocket.send(json.dumps({"type": "rate_limited"}))  # Notify user of rate limit

                else:
                    await websocket.send(json.dumps({"type": "unauthorized"}))

    # Cleanup on user disconnection
    except websockets.exceptions.ConnectionClosed:
        if websocket in CONNECTIONS:
            CONNECTIONS.remove(websocket)


async def main():
    """
    Hosts SecureChat WebSocket server on localhost:7777 indefinitely.
    """
    async with websockets.serve(securechat, "localhost", 7777):
        await asyncio.Future()  # Keep server running


if __name__ == "__main__":
    asyncio.run(main())