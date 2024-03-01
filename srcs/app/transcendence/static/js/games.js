import { SERVER_URL, doRequest } from './fetch.js';

export function getGames() {
	doRequest.Fetch(`${SERVER_URL}/api/games/`, 'GET', null, doRequest.callbackGames);
}
