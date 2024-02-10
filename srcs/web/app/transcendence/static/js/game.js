import * as JS_UTILS from './jsUtils.js';

const url = `wss://${window.location.host}/ws/matchmaking/`;
const socketMatchmaking = new WebSocket(url);

let username = null;
let matchmakingAsked = false;
const gameName = "pong";

function sendMatchmakingJoin() {
	const message = { "matchmaking": "join",
					"game": gameName, 
					"username": username };
	matchmakingAsked = true;
	JS_UTILS.sendMessageToSocket(socketMatchmaking, message);
}

function sendMatchmakingLeave() {
	const message = { "matchmaking": "leave",
					"game": gameName, 
					"username": username };
	matchmakingAsked = false;
	JS_UTILS.sendMessageToSocket(socketMatchmaking, message);
}

function sendMatchmakingStatus() {
	const message = { "matchmaking": "status",
					"game": gameName, 
					"username": username };
	JS_UTILS.sendMessageToSocket(socketMatchmaking, message);
}

function doMatchmaking(button) {
	if (button.innerHTML == "Matchmaking") {
		sendMatchmakingJoin();
	} else if (button.innerHTML == "Cancel matchmaking") {
		sendMatchmakingLeave();
	}
}

async function checkMatchmakingStatus() {
	const timeToSleep = 1000;
	while (true) {
		await new Promise(r => setTimeout(r, timeToSleep));
		if (matchmakingAsked == false) {
			return;
		}
		sendMatchmakingStatus();
	}
}

function parseMessage(message) {
	if ('matchmaking' in message) {
		const button = document.getElementById("matchmaking");
		console.log("matchmaking: " + message['matchmaking']);
		if (message['matchmaking'] == "waitlist joined") {
			button.innerHTML = "Cancel matchmaking";
			checkMatchmakingStatus();
		} 
		else if (message['matchmaking'] == "waitlist leaved") {
			button.innerHTML = "Matchmaking";
		}
		else if (message['matchmaking'] == "match found") {
			JS_UTILS.createCookie("roomID", message['socketPath'], 1);
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
			JS_UTILS.createCookie("username", username, 1);
		}
		doMatchmaking(btn);
	});
	window.addEventListener("beforeunload", function() {
		sendMatchmakingLeave();
		socketMatchmaking.close();
	});
}