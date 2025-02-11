import asyncio
import websockets
import json
import hashlib
import secrets

# Temporary user credential storage
USERS = {
    "steve": hashlib.sha256("password".encode()).hexdigest(),
    "john": hashlib.sha256("password".encode()).hexdigest(),
}

# Store connections and users
CONNECTIONS = set()
SESSIONS = {}

async def securechat(websocket):
    """
    Manages authentication and chat messaging in a secure Websocket connection. 
        - Authenticates users and establish session tokens.
        - Broadcasts messages from users
        - Handles user disconnects securely
        
    Future Improvements:
        - Securely store session tokens
        - Utilize password hashing algorithm in place of SHA256
    """
    try:
        # Listen for incoming messages from users
        async for message in websocket:
            data = json.loads(message)

            # User login authentication  
            if data["type"] == "login":
                username = data["username"]
                password = hashlib.sha256(data["password"].encode()).hexdigest()

                # Verify user login credentials and provide session tokens
                if username in USERS and USERS[username] == password:
                    session_token = secrets.token_hex(16)
                    SESSIONS[session_token] = username
                    await websocket.send(json.dumps({"type": "login_success", "token": session_token}))
                else:
                    await websocket.send(json.dumps({"type": "login_failed"}))
            
            # Handles message broadcasting
            elif data["type"] == "message":
                token = data.get("token")
                
                # Verify user session token before message processing
                if token in SESSIONS:
                    if websocket not in CONNECTIONS:
                        CONNECTIONS.add(websocket)
                    sender = SESSIONS[token]
                    full_message = f"{sender}: {data['message']}"
                    
                    # Broadcasts message to all connected users
                    websockets.broadcast(CONNECTIONS, json.dumps({"type": "message", "content": full_message}))
                else:
                    await websocket.send(json.dumps({"type": "unauthorized"}))

    # Cleanup and handle user connections
    except websockets.exceptions.ConnectionClosed:
        if websocket in CONNECTIONS:
            CONNECTIONS.remove(websocket)

async def main():
    """
    Main SecureChat function that hosts Websocket chat server on localhost port 7777 forever.
    """
    async with websockets.serve(securechat, "localhost", 7777):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())