import { doRequest } from '../utils/fetch.js';
import { callback } from '../utils/callback.js';
import { dataForm } from '../utils/data.js';

export function handleRegisterFormSubmit() {
	const form = document.getElementById('register-form');
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
        doRequest.post(`/api/register/`, data, callback.registered);
    });
};
