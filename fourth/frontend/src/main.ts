export const socket = new WebSocket("ws://localhost:8000/ws");
socket.addEventListener("open", event => {
  console.log(event);
  socket.send("Hello Server");
});

socket.addEventListener("message", event => {
  console.log("Logging received message:", event.data);
});

const input = document.getElementById("text");

if (input) {
  input.onkeydown = event => {
    if (event.key == "Enter") {
      socket.send(input.value);
      input.value = "";
    }
  };
}
