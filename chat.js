// Connect to websocket server
const ws = new WebSocket("wss://localhost:7777");

ws.onopen = () => {
    console.log("Connected to SecureChat's server");
};

ws.onmessage = (event) => {
    const chatbox = document.getElementById("chatbox");
    const message = document.createElement("div");
    message.textContent = event.data;
    chatbox.appendChild(message);
};

function sendMessage() {
    const input = document.getElementById("message");
    ws.send(input.value);
    input.value = "";
}