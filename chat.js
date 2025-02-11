let sessionToken = null;
let ws; // WebSocket instance
let reconnectAttempts = 0;
const maxReconnectAttempts = 5; // Prevent infinite reconnect loop

// Function to establish WebSocket connection
function connectWebSocket() {
    ws = new WebSocket("wss://localhost:7777"); // Secure WebSocket

    ws.onopen = () => {
        console.log("Connected to SecureChat's secure server");
        reconnectAttempts = 0; // Reset attempts on successful connection
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.type === "login_success") {
            sessionToken = data.token;
            document.getElementById("loginForm").style.display = "none";
            document.getElementById("chatInterface").style.display = "block";
        } else if (data.type === "login_failed") {
            alert("Login failed! Check your username and password.");
        } else if (data.type === "message") {
            const chatbox = document.getElementById("chatbox");
            const message = document.createElement("div");
            message.textContent = data.content;
            chatbox.appendChild(message);
        } else if (data.type === "unauthorized") {
            alert("You are not authorized to send messages.");
        } else if (data.type === "rate_limited") {
            alert("You're sending messages too fast! Please wait before sending another.");
        }
    };

    ws.onclose = () => {
        console.log("Disconnected from server. Attempting to reconnect...");

        if (reconnectAttempts < maxReconnectAttempts) {
            reconnectAttempts++;
            setTimeout(() => {
                console.log(`Reconnection attempt ${reconnectAttempts}`);
                connectWebSocket();
            }, 3000); // Retry connection after 3 seconds
        } else {
            console.log("Max reconnection attempts reached. Please refresh manually.");
        }
    };
}

// Function to handle user login
function loginUser() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    ws.send(JSON.stringify({
        type: "login",
        username: username,
        password: password
    }));
}

// Function to send chat messages
function sendMessage() {
    const input = document.getElementById("message");

    if (sessionToken) {
        ws.send(JSON.stringify({
            type: "message",
            token: sessionToken,
            message: input.value
        }));
        input.value = "";
    } else {
        alert("Please log in first.");
    }
}

// Start WebSocket connection on page load
connectWebSocket();