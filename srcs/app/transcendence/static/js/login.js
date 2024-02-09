import { SERVER_URL, doRequest } from './fetch.js';

document.addEventListener('DOMContentLoaded', function() {
	var form = document.getElementById('login-form');
	if (!form) { return; }
	form.addEventListener('submit', function(event) {
		event.preventDefault();
		var username, password, data;

		username = document.getElementById('id_username').value;
		password = document.getElementById('id_password').value;
		data = {
			'username': username,
			'password': password
		};
		doRequest.Fetch(`${SERVER_URL}/login/`, 'POST', data, doRequest.callbackLogin);
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
