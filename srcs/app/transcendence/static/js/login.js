import { SERVER_URL, doRequest } from './fetch.js';

export function handleLoginFormSubmit() {
	const form = document.getElementById('login-form');
	if (!form) { return; }
	form.addEventListener('submit', function(event) {
		event.preventDefault();

		const username = document.getElementById('username').value;
		const password = document.getElementById('password').value;
		const data = {
			'username': username,
			'password': password
		};
		doRequest.Fetch(`${SERVER_URL}/api/login/`, 'POST', data, doRequest.callbackLogin);
	});
}


// logout
export function handleLogoutFormSubmit() {
	const logoutButton = document.getElementById('logout-button');
	if (!logoutButton) { return; }
	logoutButton.addEventListener('click', function(event) {
		event.preventDefault();
		const data = {};
		doRequest.Fetch(`${SERVER_URL}/api/logout/`, 'POST', data, doRequest.callbackLogout);
		window.location.hash = 'home';
	});
	logoutButton.click();
}
