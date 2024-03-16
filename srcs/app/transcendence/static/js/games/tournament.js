import { doRequest } from '../utils/fetch.js';


export function tournamentHandler() {
	const handleClick = (event) => {
		if (event.target.matches('[id^="join-tournament-btn-"]')) {
			let tournamentId = event.target.id.split('-')[3];
			let data = { id_tournament: tournamentId };
			doRequest.post(`/api/join_tournament/`, data, (response_data) => {
				console.log(response_data);
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
			doRequest.post(`/api/create_tournament/`, data, (response_data) => {
				console.log(response_data);
			});
		}
	};

	document.body.addEventListener('click', handleClick);
	return () => document.body.removeEventListener('click', handleClick);
};

