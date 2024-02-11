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
		try {
			doRequest.Fetch(`${SERVER_URL}/login/`, 'POST', data, doRequest.callbackLogin);
			window.location.hash = 'home';
		} catch (error) {
			console.error('Une erreur est survenue lors de la connexion :', error);
			window.location.hash = 'login';
		}
	});
}


// logout
export function handleLogoutFormSubmit() {
	const logoutButton = document.getElementById('logout-button');
	if (!logoutButton) { return; }
	logoutButton.addEventListener('click', function(event) {
		event.preventDefault();
		const data = {};
		doRequest.Fetch(`${SERVER_URL}/logout/`, 'POST', data, doRequest.callbackLogout);
		window.location.hash = 'home';
	});
	logoutButton.click();
}
