import { doRequest, SERVER_URL } from '../utils/fetch.js';
import { callback } from '../utils/callback.js';
import { dataForm } from '../utils/data.js';

export function handleEditProfileFormSubmit() {
	const form = document.getElementById('profile-form');
	if (!form) { return; }
	form.addEventListener('submit', function(event) {
		event.preventDefault();

		const fields = [
			'username',
			'firstname',
			'lastname',
			'email',
			'password',
			'password_confirm',
			'avatar',
			'birthdate',
			'sexe'
		];

		const data = dataForm(fields);

		if (!data) { 
			const messageElement = document.getElementById('message');
			if (messageElement) {
				messageElement.textContent = 'Image size exceeds the limit';
			}
			return ;
		}

		doRequest.post(`${SERVER_URL}/api/edit_profile/`, data, callback.editProfile);
	});
};