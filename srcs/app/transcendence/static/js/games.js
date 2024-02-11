import { SERVER_URL, doRequest } from './fetch.js';

export function getGames() {
	doRequest.Fetch(`${SERVER_URL}/games/`, 'GET', null, console.log);
}

