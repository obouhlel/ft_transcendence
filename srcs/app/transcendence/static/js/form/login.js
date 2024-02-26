import { doRequest, SERVER_URL } from '../utils/fetch.js';

export function handleLoginFormSubmit() {
	const client_id = 'u-s4t2ud-84e176c6a1992e86e989e64db2d8abfb1aed667b9f913f5df3042bab89330f09';
	const redirectURI42 = `https://api.intra.42.fr/oauth/authorize?client_id=${client_id}&redirect_uri=${encodeURIComponent(window.location.origin + '/api/login42/')}&response_type=code`;
	console.log(redirectURI42);
	const form = document.getElementById('login-form');
	const login42 = document.getElementById('login-42');
	if (!form) { return; }
	if (!login42) { return; }

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

	login42.addEventListener('click', function(event) {
		event.preventDefault();
		window.location.href = redirectURI42;
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
	});
}
