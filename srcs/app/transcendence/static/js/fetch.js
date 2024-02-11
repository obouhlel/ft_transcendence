export const SERVER_URL = 'https://localhost:8000';

export const doRequest = {
	getCookie : function getCookie(name) {
		let cookieValue = null;
		if (document.cookie && document.cookie !== '') {
			let cookies = document.cookie.split(';');
			for (let i = 0; i < cookies.length; i++) {
				let cookie = cookies[i].trim();
				if (cookie.substring(0, name.length + 1) === (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	},

	Fetch: function(url, method, data, callback) {
		const csrftoken = this.getCookie('csrftoken');
		const options = {
			method: method,
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken,
			},
			credentials: 'include'
		};
		if (method !== 'GET' && method !== 'HEAD') {
			options.body = JSON.stringify(data);
		}
		fetch(url, options)
		.then(response => method === 'GET' ? response.text() : response.json())
		.then(data => {
			callback(data);
			setTimeout(function() {
				document.getElementById('message').textContent = '';
			}, 5000);
		})
		.catch(error => {
			console.error(error);
		});
	},

	// -------------   CALLBACKS  -------------


	callbackLogin: function(data) {
		let messageElement = document.getElementById('message');
		if (data.status === 'ok') {
			console.log('CONNEXION REUSSIE');
			doRequest.Fetch(`${SERVER_URL}/home/`, 'GET', null, doRequest.callbackHome);
			messageElement.textContent = "Connexion réussie !";
			messageElement.style.color = 'green';
		} else if (data.status === 'error') {
			console.log('ERREUR DE CONNEXION');
			document.getElementById('message').textContent = "Erreur de connexion !";
		}
	},

	callbackHome: function(data) {
		document.getElementById('section').innerHTML = data;
	},

	callbackLogout: function(data) {
		let messageElement = document.getElementById('message');
		if (data.status === 'ok') {
			console.log('DECONNEXION REUSSIE');
			messageElement.textContent = data.message;
			messageElement.style.color = 'green';
		} else if (data.status === 'error') {
			console.log('ERREUR DE DECONNEXION');
			messageElement.textContent = data.message;
			messageElement.style.color = 'red';
		}
	},

	callbackRegister: function(data) {
		let messageElement = document.getElementById('message');
		if (data.status === 'ok') {
			console.log('INSCRIPTION REUSSIE');
			messageElement.textContent = data.message;
			messageElement.style.color = 'green';
		} else if (data.status === 'error') {
			console.log('ERREUR D\'INSCRIPTION');
			messageElement.textContent = data.message;
			messageElement.style.color = 'red';
		}
	},

};
