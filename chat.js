// Establish a connection to SecureChat websocket
const ws = new WebSocket("ws://localhost:7777");

// Store session token after login
let sessionToken = null; 

// Message on successful connection to server
ws.onopen = () => {
    console.log("Connected to SecureChat's server");
};

// Event handler for incoming messages from the SecureChat server
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    // Handles successful login
    if (data.type === "login_success") {
        sessionToken = data.token;
        document.getElementById("loginForm").style.display = "none";
        document.getElementById("chatInterface").style.display = "block";

    // Handles failed login attempts
    } else if (data.type === "login_failed") {
        alert("Login failed! Check your username and password.");

    // Displays messages sent in chatbox
    } else if (data.type === "message") {
        const chatbox = document.getElementById("chatbox");
        const message = document.createElement("div");
        message.textContent = data.content;
        chatbox.appendChild(message);

    // Handles unauthorized message attemps
    } else if (data.type === "unauthorized") {
        alert("You are not authorized to send messages.");
    }
};

// Function for user login handling
function loginUser() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // Sends user login request to SecureChat server
    ws.send(JSON.stringify({
        type: "login",
        username: username,
        password: password
    }));
}

// Function for message sending
function sendMessage() {
    const input = document.getElementById("message");

    // Checks if user session is authenticated before sending message
    if (sessionToken) {
        ws.send(JSON.stringify({
            type: "message",
            token: sessionToken,
            message: input.value
        }));
        input.value = ""; // Clears input field after sending message
    } else {
        alert("Please log in first.");
    }
}
