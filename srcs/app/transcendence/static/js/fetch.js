// export const SERVER_URL = 'https://localhost:8000';
export const SERVER_URL = '';

export const doRequest = {
	getCookie: function getCookie(name)
	{
		let cookieValue = null;
		if (document.cookie && document.cookie !== '')
		{
			let cookies = document.cookie.split(';');
			for (let i = 0; i < cookies.length; i++)
			{
				let cookie = cookies[i].trim();
				if (cookie.substring(0, name.length + 1) === (name + '='))
				{
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	},

	Fetch: function(url, method, data, callback)
	{
		const csrftoken = this.getCookie('csrftoken');
		const options = {
			method: method,
			headers: {'X-CSRFToken': csrftoken},
			credentials: 'include'
		};
		if (data instanceof FormData)
		{
			options.body = data;
		}
		else if (method !== 'GET' && method !== 'HEAD')
		{
			options.headers['Content-Type'] = 'application/json';
			options.body = JSON.stringify(data);
		}
		fetch(url, options)
		.then(response => response.json())
		.then(data => {
			callback(data);
			setTimeout(function() {
				if (document.getElementById('message'))
					document.getElementById('message').textContent = '';
			}, 5000);
		})
		.catch(error => {console.error(error);});
	},

	// -------------   CALLBACKS  -------------


	callbackLogin: function(data)
	{
		let messageElement = document.getElementById('message');
		if (!messageElement)
			return console.error('Element with class "message" not found');
		if (data.status === 'ok')
		{
			console.log('CONNEXION REUSSIE');
			window.location.hash = 'games';
		}
		else if (data.status === 'error')
		{
			console.log('ERREUR DE CONNEXION');
			window.location.hash = 'login';
			messageElement.textContent = data.message;
		}
	},

	callbackLogout: function(data)
	{
		if (data.status === 'ok')
		{
			console.log('DECONNEXION REUSSIE');
			window.location.hash = 'login';
		}
		else if (data.status === 'error')
		{
			console.log('ERREUR DE DECONNEXION');
		}
	},

	callbackRegister: function(data)
	{
		let messageElement = document.getElementById('message');
		if (!messageElement)
			return console.error('Element with class "message" not found');
		if (data.status === 'ok')
		{
			console.log('INSCRIPTION REUSSIE');
			messageElement.textContent = data.message;
			messageElement.style.color = 'green';
			window.location.hash = 'login';
		}
		else if (data.status === 'error')
		{
			console.log('ERREUR D\'INSCRIPTION');
			messageElement.textContent = data.message;
			messageElement.style.color = 'red';
		}
	},

	callbackProfile: function(data)
	{
		let messageElement = document.getElementById('message');
		if (!messageElement)
			return console.error('Element with class "message" not found');
		if (data.status === 'ok')
		{
			console.log('MODIFICATION REUSSIE');
			window.location.hash = 'profile';
		}
		else if (data.status === 'error')
		{
			console.log('ERREUR DE MODIFICATION');
			messageElement.textContent = data.message;
			messageElement.style.color = 'red';
		}
	},

	callbackGames: function(data) {
		let messageElement = document.getElementById('message');
		if (!messageElement)
			return console.error('Element with class "message" not found');
		if (data.status === 'ok')
		{
			console.log('GAMES REUSSIE');
		}
		else if (data.status === 'error')
		{
			console.log('ERREUR DE GAMES');
		}
	},
};
