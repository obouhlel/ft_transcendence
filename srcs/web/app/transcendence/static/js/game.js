import * as JS_UTILS from './jsUtils.js';

const url = `wss://${window.location.host}/ws/matchmaking/`;
const socketMatchmaking = new WebSocket(url);

let username = null;

let registered = false;
const gameName = "pong";

function sendRegister() {
	const message = {
		"register": "in",
		"username": username
	};
	JS_UTILS.sendMessageToSocket(socketMatchmaking, message);
}

function sendUnregister() {
	const message = {
		"register": "out",
		"username": username
	};
	JS_UTILS.sendMessageToSocket(socketMatchmaking, message);
}

function sendMatchmakingJoin() {
	const message = { 
		"matchmaking": "join",
		"game": gameName, 
		"username": username 
	};
	JS_UTILS.sendMessageToSocket(socketMatchmaking, message);
}

function sendMatchmakingLeave() {
	const message = { 
		"matchmaking": "leave",
		"game": gameName, 
		"username": username 
	};
	JS_UTILS.sendMessageToSocket(socketMatchmaking, message);
}

function doMatchmaking(button) {
	if (button.innerHTML == "Matchmaking") {
		if (!registered)
			sendRegister();
		else
			sendMatchmakingJoin();
	} else if (button.innerHTML == "Cancel matchmaking") {
		if (registered)
			sendUnregister();
		else
			sendMatchmakingLeave();
	}
}

function parseMessage(message) {
	if ('register' in message) {
		if (message['register'] == "connected") {
			registered = true;
			sendMatchmakingJoin();
		}
		else if (message['register'] == "disconnected") {
			registered = false;
			sendMatchmakingLeave();
		}
	}
	if ('matchmaking' in message) {
		const button = document.getElementById("matchmaking");
		if (message['matchmaking'] == "waitlist joined") {
			button.innerHTML = "Cancel matchmaking";
		} 
		else if (message['matchmaking'] == "waitlist leaved") {
			button.innerHTML = "Matchmaking";
		}
		else if (message['matchmaking'] == "match found") {
			JS_UTILS.createCookie("url", message['url'], 1);
			const url = window.location.href;
			let segments = url.split('/');
			segments[segments.length - 2] = message['game'];
			const gameURL = segments.join('/');
			window.location.href = gameURL;
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
		console.log(`socketMatchmaking error: ${error}`);
		console.error(error);
	}
}	

export function listenerGame() {
	const btn = document.getElementById("matchmaking");
	btn.addEventListener("click", function() {
		if (username == null) {
			username = document.getElementById("username").value;
			JS_UTILS.createCookie("username", username, 1);
		}
		doMatchmaking(btn);
	});
	window.addEventListener("beforeunload", function() {
		sendMatchmakingLeave();
		socketMatchmaking.close();
	});
}