const url = `wss://${window.location.host}/ws/matchmaking/`;
const socketMatchmaking = new WebSocket(url);

function send_message(textMessage) {
	var message = { "message": textMessage };
	socketMatchmaking.send(JSON.stringify(message));
	console.log("Sent message: " + JSON.stringify(message));
}

export function game()
{
	
	socketMatchmaking.onopen = function(e) {
		console.log("Connection established");
	}
	
	socketMatchmaking.onmessage = function(e) {
		let data = JSON.parse(e.data);
		console.log("Received message: " + e.data);
	}
	
	socketMatchmaking.onclose = function(e) {
		console.log("Connection closed");
	}
	
	socketMatchmaking.onerror = function(error) {
		console.log(`socketMatchmaking error: ${event}`);
		console.error(event);
	}
}	

export function listenerGame() {
    const btn = document.getElementById("matchmaking");
    btn.addEventListener("click", send_message("request matchmaking"));
}