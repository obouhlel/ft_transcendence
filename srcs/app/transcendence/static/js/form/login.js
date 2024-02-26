import { doRequest, SERVER_URL } from '../utils/fetch.js';
import { callback } from '../utils/callback.js';

export function handleLoginFormSubmit() {
	const client_id = 'u-s4t2ud-19bb21faf559dbd098d85eea58ab84e1a45b6f5e10a0008bac8679bac0c91d1a';
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

		console.log(data);
		doRequest.post(`${SERVER_URL}/api/login/`, data, callback.login);
	});

	login42.addEventListener('click', function(event) {
		event.preventDefault();
		window.location.href = redirectURI42;
	});
}
