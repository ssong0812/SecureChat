// Establish a secure WebSocket connection
const ws = new WebSocket("wss://localhost:7777");

// Store session token after login
let sessionToken = null; 

// Message on successful connection to server
ws.onopen = () => {
    console.log("Connected securely to SecureChat's server");
};

// Event handler for incoming messages
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
    }
};

// Function for user login handling
function loginUser() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    ws.send(JSON.stringify({
        type: "login",
        username: username,
        password: password
    }));
}

// Function for sending messages
function sendMessage() {
    const input = document.getElementById("message");

    if (sessionToken) {
        ws.send(JSON.stringify({
            type: "message",
            token: sessionToken,
            message: input.value
        }));
        input.value = ""; // Clear input field
    } else {
        alert("Please log in first.");
    }
}