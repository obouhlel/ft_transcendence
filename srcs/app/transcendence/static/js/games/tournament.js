import { doRequest } from '../utils/fetch.js';


export function tournamentHandler() {
	const handleClick = (event) => {
		if (event.target.matches('.join-tournament-btn')) {
			let data = { id_tournament: event.target.dataset.tournamnetId };
			doRequest.post(`/api/join_tournament/`, data, (reponse_data) => {
				console.log(reponse_data);
			});
		}
	};
	document.body.addEventListener('click', handleClick);
	return () => document.body.removeEventListener('click', handleClick);
}


export const createTournamentHandler = () => {
	const handleClick = (event) => {
		if (event.target.matches('.create-tour-btn')) {
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

