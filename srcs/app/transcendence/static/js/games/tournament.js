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
		if (event.target.matches('.join-tournament-btn')) {
			console.log(event.target.dataset);
			let data = { id_tournament: event.target.dataset.tournamentId };
			doRequest.post(`/api/join_tournament/`, data, (reponse_data) => {
				event.target.innerHTML = "Leave";
				event.target.classList.remove("join-tournament-btn");
				event.target.classList.add("leave-tournament-btn");
				console.log(reponse_data);
			});
		}
		else if (event.target.matches('.leave-tournament-btn')) {
			let data = { id_tournament: event.target.dataset.tournamentId };
			doRequest.post(`/api/leave_tournament/`, data, (reponse_data) => {
				event.target.innerHTML = "Join";
				event.target.classList.remove("leave-tournament-btn");
				event.target.classList.add("join-tournament-btn");
				console.log(reponse_data);
			});
		}
	};
	document.body.addEventListener('click', handleClick);
	return () => document.body.removeEventListener('click', handleClick);
}


export const createTournamentHandler = () => {
	console.log('createTournamentHandler');
	const handleClick = (event) => {
		if (event.target.matches('.create-tour-btn')) {
			let data = {
				name: document.getElementById('tour-name').value,
				nb_players: parseInt(document.getElementById('nb_players').value),
				id_game: parseInt(document.getElementById('game_id').value)
			};
			doRequest.post(`/api/create_tournament/`, data, (response_data) => {
				if (response_data.status === 'ok') {
					window.location.hash = `tournament?id=${data.id_game}`;
				}
			});
		}
	};

	document.body.addEventListener('click', handleClick);
	return () => document.body.removeEventListener('click', handleClick);
};

