import { SERVER_URL, doRequest } from './fetch.js';

export function getGames() {
	return doRequest(`${SERVER_URL}/games`);
}

