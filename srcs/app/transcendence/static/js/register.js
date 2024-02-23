import { doRequest, SERVER_URL } from './fetch.js';

export function handleRegisterFormSubmit() {
    const client_id = 'u-s4t2ud-5b9c9133859a5333ef620d8fd41e79e5ce3174c4300678ff79c6f12c88a4cf77';
	const redirectURI42 = `https://api.intra.42.fr/oauth/authorize?client_id=${client_id}&redirect_uri=https%3A%2F%2Flocalhost%3A8000%2Fapi%2Flogin42%2F&response_type=code`;
    const form = document.getElementById('register-form');
    const login42 = document.getElementById('login-42');
    const login = document.getElementById('login');
    if (!form) { return; }

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const fields = ['username', 'firstname', 'lastname', 'email', 'password', 'password_confirm', 'avatar', 'birthdate', 'sexe'];
        let data = new FormData();

		fields.forEach(field => {
			let element = document.getElementById(field);
			if (element) {
				let value = field === 'avatar' ? element.files[0] : element.value;
				data.append(field, value);
			} else {
				console.log(`Element with ID ${field} not found`);
			}
		});
        try {
            console.log('data register:', Object.fromEntries(data.entries()));
            doRequest.Fetch(`${SERVER_URL}/api/register/`, 'POST', data, doRequest.callbackRegister);
            window.location.hash = 'login';
        }
        catch (error) {
            console.error('Une erreur est survenue lors de l\'inscription :', error);
            window.location.hash = 'register';
        }
    });

    login42.addEventListener('click', function(event) {
		event.preventDefault();
		window.location.href = redirectURI42;
	});

    login.addEventListener('click', function(event) {
        event.preventDefault();
        window.location.href = '#login';
    });
};
