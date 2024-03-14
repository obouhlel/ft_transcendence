import { doRequest } from '../utils/fetch.js';

export function GameHandler() {
	const handleClick = (event) => {
		if (event.target.matches('.matchmaking-btn')) {
			console.log('matchmaking');
			console.log(event.target.dataset.gameId);
			let data = {id_game: event.target.dataset.gameId};
			doRequest.post(`/api/join_lobby/`, data, (response_data) => {
				console.log(response_data);
			});
		}
	}
	document.body.addEventListener('click', handleClick);
	return () => document.body.removeEventListener('click', handleClick);
}