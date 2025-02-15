import asyncio
import websockets
import json
import hashlib
import secrets
import ssl
import time
from collections import defaultdict

# Load SSL certificate and key
SSL_CONTEXT = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
SSL_CONTEXT.load_cert_chain(certfile="localhost.pem", keyfile="localhost-key.pem")

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

# Message storage for persistence
MESSAGE_STORAGE = []

async def securechat(websocket):
    """Handles WebSocket connections securely."""
    try:
        async for message in websocket:
            data = json.loads(message)

            # User registration
            if data["type"] == "register":
                username = data["username"]
                password = hashlib.sha256(data["password"].encode()).hexdigest()

                if username in USERS:
                    await websocket.send(json.dumps({"type": "register_failed", "message": "Username already exists."}))
                else:
                    USERS[username] = password
                    await websocket.send(json.dumps({"type": "register_success", "message": "Registration successful. Please log in."}))

            # User login authentication
            elif data["type"] == "login":
                username = data["username"]
                password = hashlib.sha256(data["password"].encode()).hexdigest()

                if username in USERS and USERS[username] == password:
                    session_token = secrets.token_hex(16)
                    SESSIONS[session_token] = username
                    await websocket.send(json.dumps({"type": "login_success", "token": session_token}))

                    # Send chat history to the user upon login
                    await websocket.send(json.dumps({"type": "chat_history", "messages": MESSAGE_STORAGE}))
                else:
                    await websocket.send(json.dumps({"type": "login_failed"}))

            # Handle message broadcasting with rate limiting
            elif data["type"] == "message":
                token = data.get("token")

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
                        MESSAGE_STORAGE.append(full_message)  # Store message in history
                        websockets.broadcast(CONNECTIONS, json.dumps({"type": "message", "content": full_message}))
                    else:
                        await websocket.send(json.dumps({"type": "rate_limited", "message": f"Rate limit exceeded. Please wait {MESSAGE_WINDOW} seconds."}))
                else:
                    await websocket.send(json.dumps({"type": "unauthorized"}))

    except websockets.exceptions.ConnectionClosed:
        if websocket in CONNECTIONS:
            CONNECTIONS.remove(websocket)

async def main():
    """Starts the SecureChat WebSocket server with SSL."""
    async with websockets.serve(securechat, "localhost", 7777, ssl=SSL_CONTEXT):
        await asyncio.Future()  # Keep server running

if __name__ == "__main__":
    asyncio.run(main())