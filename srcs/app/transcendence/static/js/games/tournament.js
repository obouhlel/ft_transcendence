import { doRequest } from '../utils/fetch.js';


export function tournamentHandler() {
	const handleClick = (event) => {
		const leaveButtons = document.querySelectorAll('[id^="leave-tournament-btn-"]');
		if (event.target.matches('[id^="join-tournament-btn-"]')) {
			if (leaveButtons.length > 0) {
				console.error('Invalid button clicked');
				const messageElement = document.getElementById('message');
				if (!messageElement)
					return console.error('Element with id "message" not found');
				messageElement.textContent = 'You can only one join a tournament';
				return;
			}
			let tournamentId = event.target.id.split('-')[3];
			let data = { id_tournament: tournamentId };
			doRequest.post(`/api/join_tournament/`, data, (response_data) => {
				console.log(response_data);
				if (response_data.status === 'ok')
					window.location.hash = 'lobby-tournament?id=' + tournamentId;
				else if (response_data.status === 'error') {
					const messageElement = document.getElementById('message');
					if (!messageElement)
						return console.error('Element with id "message" not found');
					messageElement.textContent = response_data.message;
				}
			});
		}
		else if (event.target.matches('[id^="leave-tournament-btn-"]')) {
			let tournamentId = event.target.id.split('-')[3];
			let data = { id_tournament: tournamentId };
			doRequest.post(`/api/leave_tournament/`, data, (response_data) => {
				console.log(response_data);
			});
		}
	};
	document.body.addEventListener('click', handleClick);
	return () => document.body.removeEventListener('click', handleClick);
}

export const createTournamentHandler = () => {
	const handleClick = (event) => {
		if (event.target.matches('#create')) {
			let data = { 
				name: document.getElementById('tour-name').value,
				nb_players: parseInt(document.getElementById('nb_players').value),
				id_game: parseInt(document.getElementById('game_id').value)
			};
			doRequest.post(`/api/create_tournament/`, data, (data) => {
				console.log(data);
				if (data.status === 'ok') {
					window.location.hash = 'lobby-tournament?id=' + data.id_tournament;
				}
				else if (data.status === 'error') {
					const messageElement = document.getElementById('message');
					if (!messageElement)
						return console.error('Element with class "message" not found');
					messageElement.textContent = data.message;
				}
			});
		}
	};

	document.body.addEventListener('click', handleClick);
	return () => document.body.removeEventListener('click', handleClick);
};

