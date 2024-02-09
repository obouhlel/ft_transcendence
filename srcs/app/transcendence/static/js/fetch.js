export const SERVER_URL = 'https://localhost:8000';

export const doRequest = {
	getCookie : function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie !== '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = cookies[i].trim();
				if (cookie.substring(0, name.length + 1) === (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	},

	Fetch: function(url, method, data, callback) {
		var csrftoken = this.getCookie('csrftoken');
		fetch(url, {
			method: method,
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken,
				'Accept': 'application/json'
			},
			credentials: 'include',
			body: ['HEAD', 'GET'].includes(method.toUpperCase())  ? undefined : JSON.stringify(data)
		})
		.then(response => response.json())
		.then(data => {
			callback(data);
		})
		.catch(error => {
			console.error(error);
		});
	},

	// -------------   CALLBACKS  -------------


	callbackLogin: function(data) {
		var messageElement = document.getElementById('message');
		if (data.status === 'ok') {
			console.log('CONNEXION REUSSIE');
			messageElement.textContent = data.message;
			messageElement.style.color = 'green';
			window.location.reload();
		} else if (data.status === 'error') {
			console.log('ERREUR DE CONNEXION');
			messageElement.textContent = data.message;
			messageElement.style.color = 'red';
		}
	},

	callbackLogout: function(data) {
		var messageElement = document.getElementById('message');
		if (data.status === 'ok') {
			console.log('DECONNEXION REUSSIE');
			messageElement.textContent = data.message;
			messageElement.style.color = 'green';
			window.location.reload();
		} else if (data.status === 'error') {
			console.log('ERREUR DE DECONNEXION');
			messageElement.textContent = data.message;
			messageElement.style.color = 'red';
		}
	},

	callbackRegister: function(data) {
		var messageElement = document.getElementById('message');
		if (data.status === 'ok') {
			console.log('INSCRIPTION REUSSIE');
			messageElement.textContent = data.message;
			messageElement.style.color = 'green';
		} else if (data.status === 'error') {
			console.log('ERREUR D\'INSCRIPTION');
			messageElement.textContent = data.message;
			messageElement.style.color = 'red';
		}
	}
};
