import { SERVER_URL, doRequest } from './fetch.js';

document.addEventListener('DOMContentLoaded', function() {
	const form = document.getElementById('profile-form');
	if (!form) { return; }
	form.addEventListener('submit', function(event) {
		event.preventDefault();

		const fields = ['username', 'firstname', 'lastname', 'email', 'password', 'password_confirm', 'avatar', 'birthdate', 'sexe'];

		let data = new FormData();
		fields.forEach(field => {
			let value = field === 'avatar' ? document.getElementById(field).files[0] : document.getElementById(field).value;
			data.append(field, value);
		});

		doRequest.Fetch(`${SERVER_URL}/edit_profile/`, 'POST', data, doRequest.callbackProfile);
	});
});
