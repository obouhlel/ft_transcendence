import { doRequest, SERVER_URL } from '../utils/fetch.js';
import { callback } from '../utils/callback.js';

export function handleLogout() {
	const logoutButton = document.getElementById('logout-button');
	if (!logoutButton) { return; }
	logoutButton.addEventListener('click', function(event) {
		event.preventDefault();
		doRequest.post(`${SERVER_URL}/api/logout/`, {}, callback.logout);
	});
}