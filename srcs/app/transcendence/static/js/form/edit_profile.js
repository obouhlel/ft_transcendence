import { doRequest } from '../utils/fetch.js';
import { callback } from '../utils/callback.js';
import { dataForm } from '../utils/data.js';

export function handleEditProfileFormSubmit() {
	const form = document.getElementById('profile-form');
	const uploadField = document.getElementById("avatar");
	if ( !form || !uploadField ) { return; }

	uploadField.onchange = function() {
		if(this.files[0].size > 1048576) {
			const messageElement = document.getElementById('message');
			if (messageElement) {
				messageElement.innerHTML = "File is too big! Max size is 1MB!";
			}
			this.value = "";
		}
	};

	form.addEventListener('submit', function(event) {
		event.preventDefault();

		const fields = [
			'avatar',
			'username',
			'firstname',
			'lastname',
			'email',
			'password',
		];

		const data = dataForm(fields);

		doRequest.post(`/api/edit_profile/`, data, callback.editProfile);
	});
}

export function handleChangePassword() {
	const form = document.getElementById('password-form');
	if ( !form ) { return; }

	form.addEventListener('submit', function(event) {
		event.preventDefault();

		const fields = [
			'old_password',
			'new_password',
			'confirm_password',
		];

		const data = dataForm(fields);

		doRequest.post(`/api/change_password/`, data, (data) => {
			if (data.status === 'ok')
			{
				window.location.hash = '#profile';
			}
			else if (data.status === 'error')
			{
				const messageElement = document.getElementById('message');
				if (messageElement) {
					messageElement.innerHTML = data.message;
				}
			}
		});
	});
}