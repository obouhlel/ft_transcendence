export function game()
{
	const url = `wss://${window.location.host}/ws/matchmaking/`;
	const socketMatchmaking = new WebSocket(url);
	
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

	function send_message() {
		var message = { "message": "Hello, world!" };
		socketMatchmaking.send(JSON.stringify(message));
		console.log("Sent message: " + JSON.stringify(message));
	}
	
	const btn = document.getElementById("matchmaking");
	if (btn)
	{
		btn.addEventListener("click", send_message);
	}
}	
