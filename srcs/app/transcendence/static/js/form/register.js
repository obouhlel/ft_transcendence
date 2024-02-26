import { doRequest, SERVER_URL } from '../utils/fetch.js';
import { callback } from '../utils/callback.js';

export function handleRegisterFormSubmit() {
    const form = document.getElementById('register-form');
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
        let data = new FormData();

		fields.forEach(field => {
			let element = document.getElementById(field);
			if (element) {
				let value = field === 'avatar' ? element.files[0] : element.value;
				data.append(field, value);
			}
            else {
				console.log(`Element with ID ${field} not found`);
			}
		});

        doRequest.post(`${SERVER_URL}/api/register/`, data, callback.registered);
    });
};
