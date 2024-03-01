import { doRequest, SERVER_URL } from '../utils/fetch.js';
import { callback } from '../utils/callback.js';

export function handleLoginFormSubmit() {
	// Login form
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

		doRequest.post(`${SERVER_URL}/api/login/`, data, callback.login);
	});
	// 42 login
	const url_42 = 'https://api.intra.42.fr/oauth/authorize';
	const client_id = 'u-s4t2ud-ecdf3141d39f400a2eef9675f111895a2583c1233a58a5ac0eebadd15ffb8e9e';
	const redirect_uri = encodeURIComponent(window.location.origin + '/api/login_42/');
	const url = `${url_42}?client_id=${client_id}&redirect_uri=${redirect_uri}&response_type=code`;
	const login42 = document.getElementById('login-42');
	if (!login42) { return; }
	login42.addEventListener('click', function(event) {
		event.preventDefault();
		window.location.href = url;
	});
}
