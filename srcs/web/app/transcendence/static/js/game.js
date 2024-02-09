const url = `wss://${window.location.host}/ws/matchmaking/`;
const socketMatchmaking = new WebSocket(url);

let username = null;
const gameName = "pong";

function sendMatchmakingJoin() {
	const message = { "matchmaking": "join",
					"game": gameName, 
					"username": username };
	socketMatchmaking.send(JSON.stringify(message));
	console.log("Sent message: " + JSON.stringify(message));
}

function sendMatchmakingLeave() {
	const message = { "matchmaking": "leave",
					"game": gameName, 
					"username": username };
	socketMatchmaking.send(JSON.stringify(message));
	console.log("Sent message: " + JSON.stringify(message));
}

function doMatchmaking(button) {
	if (button.innerHTML == "Matchmaking") {
		sendMatchmakingJoin();
		button.innerHTML = "Cancel matchmaking";

	} else if (button.innerHTML == "Cancel matchmaking") {
		sendMatchmakingLeave();
		button.innerHTML = "Matchmaking";
	}
}

function parseMessage(message) {
	if ('matchmaking' in message) {
		if (message['matchmaking'] == "waitlist joined") {
			console.log("Waitlist joined successfully");
		} else if (message['matchmaking'] == "waitlist leaved") {
			console.log("Waitlist leaved successfully");
		}
	}
}

export function game()
{
	socketMatchmaking.onopen = function(e) {
		console.log("Connection established");
	}
	
	socketMatchmaking.onmessage = function(e) {
		let data = JSON.parse(e.data);
		console.log("Received message: " + e.data);
		parseMessage(data);
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
    btn.addEventListener("click", function() {
		if (username == null) {
			console.log("username is null");
			username = document.getElementById("username").value;
		}
		doMatchmaking(btn);
	});
}