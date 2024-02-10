import { SERVER_URL, doRequest } from './fetch.js';

document.addEventListener('DOMContentLoaded', function() {
	var form = document.getElementById('login-form');
	if (!form) { return; }
	form.addEventListener('submit', function(event) {
		event.preventDefault();
		var username, password, data;

		username = document.getElementById('username').value;
		password = document.getElementById('password').value;
		data = {
			'username': username,
			'password': password
		};
		console.log('data:', data);
		// try {
        //     doRequest.Fetch(`${SERVER_URL}/login/`, 'POST', data, doRequest.callbackLogin);
        // } catch (error) {
        //     console.error('Une erreur est survenue lors de la connexion :', error);
        // }
	});
});


// logout
document.addEventListener('DOMContentLoaded', function() {
	var logoutButton = document.getElementById('logout-button');
	if (!logoutButton) { return; }
	logoutButton.addEventListener('click', function(event) {
		event.preventDefault();
		var data = {};
		doRequest.Fetch(`${SERVER_URL}/logout/`, 'POST', data, doRequest.callbackLogout);
	});
});
