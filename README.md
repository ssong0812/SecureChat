# SecureChat
Simple WebSocket implementation in Python for live chatting.

You are a security tooling analyst working for SecureTech Solutions, a company specializing in software for distributed teams. The company is developing a real-time communication tool called SecureChat, aimed at remote teams that require secure and efficient communication without relying on third-party services like Slack or Teams. Your task is to design and implement the communication system for SecureChat, focusing on secure WebSocket-based communication.

# Scope

SecureChat will serve as a foundational product for SecureTech’s offerings. The first version of the system will be a proof-of-concept (POC):

    A client-server WebSocket-based chat system that allows team members to communicate in real time. For the POC, you must have 2 users communicating on the system.
    Bonus: Functionality to transfer files (documents, images, etc.)
        Hint: Explore other protocols such as FTP

# Key Features

  1. Real-Time Messaging
  2. Secure Connection
  3. User Authentication
  4. Rate Limiting
  5. Connection Handling

# Usage

Ensure you have Python 3.8 or later installed on your system

Additionally, install the python websockets library with the following command:

      pip install websockets

As SecureChat is in its first stage, the user must generate a self-signed certificate. To do so run the command:

      openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes

Next start the SecureChat server with the command:

      python3 server.py

You can now open the client.html file on your browser.
