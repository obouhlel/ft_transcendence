import { SERVER_URL, doRequest } from './fetch.js';

export function getGames() {
	const response = doRequest.get(`${SERVER_URL}/api/games/`);
	console.log(response);
}
