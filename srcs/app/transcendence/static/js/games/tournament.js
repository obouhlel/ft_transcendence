import { doRequest } from '../utils/fetch.js';

export async function tournamentHandler() {

	let socket = new WebSocket(
		"wss://" + window.location.host + "/ws/tournament/" + window.location.hash.split('=')[1],
	);

	socket.onopen = function(event) {
		console.log('###### WebSocket tournament connection opened #####');
	}

	socket.onclose = function(event) {
		console.log('###### WebSocket tournament connection closed ######');
	}

	socket.onmessage = function(event) {
		let data = JSON.parse(event.data);
		let message = data.message;

		console.log('###### WebSocket tournament message received:', message);

		// If the message is the current player count, update the display
		if (message.action === 'Update Player Count') {
			console.log('###### Update Player Count ######');
			let playerCount = message.playerCount;
			let maxPlayerCount = message.maxPlayerCount;
			let tournamentId = message.tournamentId;

			// Update the player count display
			let playerCountElement = document.getElementById(`player-count-${tournamentId}`);
			if (playerCountElement) {
				playerCountElement.textContent = `${playerCount}/${maxPlayerCount}`;
			}
		}
		else
		{
			console.log('###### Other message ###### :', message);
		}
	};

	const handleClick = (event) => {
		const leaveButtons = document.querySelectorAll('[id^="leave-tournament-btn-"]');
		if (event.target.matches('[id^="join-tournament-btn-"]')) {
			if (leaveButtons.length > 0) {
				console.error("Invalid button clicked");
				const messageElement = document.getElementById("message");
				if (!messageElement)
					return console.error('Element with id "message" not found');
				messageElement.textContent = "You can only one join a tournament";
				return;
			}
			let tournamentId = event.target.id.split("-")[3];
			let data = { id_tournament: tournamentId };
			doRequest.post(`/api/join_tournament/`, data, (response_data) => {
				console.log(response_data);
				if (response_data.status === "ok")
					window.location.hash =
						"lobby-tournament?id=" + tournamentId;
				else if (response_data.status === "error") {
					const messageElement = document.getElementById("message");
					if (!messageElement)
						return console.error('Element with id "message" not found');
					messageElement.textContent = response_data.message;
				}
			});
		}
		else if (event.target.matches('[id^="leave-tournament-btn-"]')) {
			let tournamentId = event.target.id.split("-")[3];
			let data = { id_tournament: tournamentId };
			doRequest.post(`/api/leave_tournament/`, data, (response_data) => {
				console.log(response_data);
			});
		}
	};
	document.body.addEventListener("click", handleClick);
	return () => document.body.removeEventListener("click", handleClick);
}

export const createTournamentHandler = () => {
	const handleClick = (event) => {
		if (event.target.matches("#create")) {
			let data = {
				name: document.getElementById("tour-name").value,
				nb_players: parseInt(document.getElementById("nb_players").value),
				id_game: parseInt(document.getElementById("game_id").value),
			};
			doRequest.post(`/api/create_tournament/`, data, (data) => {
				console.log(data);
				if (data.status === "ok") {
					window.location.hash = "lobby-tournament?id=" + data.id_tournament;
				}
				else if (data.status === "error") {
					const messageElement = document.getElementById("message");
					if (!messageElement)
						return console.error('Element with class "message" not found');
					messageElement.textContent = data.message;
				}
			});
		}
	};

	document.body.addEventListener("click", handleClick);
	return () => document.body.removeEventListener("click", handleClick);
};

export function aliasFormsHandler() {
	const aliasForms = document.getElementById("alias-forms");
	if (!aliasForms)
		return console.error('Element with id "alias-forms" not found');
	const handleSubmit = (event) => {
		event.preventDefault();

		const alias = document.getElementById("alias").value;
		const data = { alias: alias };
		doRequest.post(`/api/alias/`, data, (response) => {
			console.log(response);
			const messageElement = document.getElementById("message");
			if (!messageElement)
				return console.error('Element with class "message" not found');
			if (response.status === "ok") {
				messageElement.textContent = response.message;
			}
			else if (response.status === "error") {
				messageElement.textContent = response.message;
			}
		});
	};
	aliasForms.addEventListener("submit", handleSubmit);
}

export async function tournamentLobbyHandler() {
	const tournamentId = window.location.hash.split("id=")[1];
	const hashage = window.location.hash.split("?")[0];
	console.log("Tournament id: ", tournamentId);
	const data = await doRequest.get(`/api/get_tournament_by_id/${tournamentId}`);
	console.log(data);
	const messageElement = document.getElementById("message");
	if (!messageElement)
		return console.error('Element with id "message" not found');
	if (data.status === "error") {
		messageElement.textContent = data.message;
		return;
	}
	const tournament = data.tournament;
	const nb_players = tournament.users.length;
	const nb_players_max = tournament.nb_player_to_start;
	console.log("Nb players: ", nb_players);
	console.log("Nb players max: ", nb_players_max);
	console.log("Tournament: ", tournament);
	const handleClickStart = (event) => {
		if (nb_players === nb_players_max)
		{
			messageElement.textContent = "Starting the tournament...";
			// RUN WEBSOCKET
		}
		else
		{
			messageElement.textContent = "Need more players to start the tournament";
		}
	}
	const handleClickLeave = (event) => {
		const gameId = tournament.id_game;
		doRequest.post(`/api/leave_tournament/`, { id_tournament: tournamentId }, (response) => {
			console.log(response);
			if (response.status === "ok")
				window.location.hash = "tournament?id=" + gameId;
			else if (response.status === "error") {
				messageElement.textContent = response.message;
			}
		});
	}
	const handleHashChange = (event) => {
		const newHash = window.location.hash.split("?")[0];
		if (newHash !== "#lobby-tournament") {
			const data = { id_tournament: tournamentId };
			doRequest.post(`/api/leave_tournament/`, data);
		}
	};

	const handleLoad = (event) => {
		const currentHash = window.location.hash.split("?")[0];
		if (currentHash === "#lobby-tournament") {
			const data = { id_tournament: tournamentId };
			doRequest.post(`/api/join_tournament/`, data);
		}
	};
	window.addEventListener("hashchange", handleHashChange);
	window.addEventListener("load", handleLoad);
	const startButton = document.getElementById("start-tournament");
	if (startButton)
		startButton.addEventListener("click", handleClickStart);
	const leaveButton = document.getElementById("leave-tournament");
	if (leaveButton)
		leaveButton.addEventListener("click", handleClickLeave);
}
