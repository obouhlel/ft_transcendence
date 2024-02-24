import { SERVER_URL, doRequest } from './fetch.js';

export function handleLoginFormSubmit() {
	const client_id = 'u-s4t2ud-5b9c9133859a5333ef620d8fd41e79e5ce3174c4300678ff79c6f12c88a4cf77';
	const redirectURI42 = `https://api.intra.42.fr/oauth/authorize?client_id=${client_id}&redirect_uri=https%3A%2F%2Flocalhost%3A8000%2Fapi%2Flogin42%2F&response_type=code`;
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
