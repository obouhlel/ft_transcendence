export const callback = {
	login: function(data)
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

	logout: function(data)
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

	registered: function(data)
	{
		let messageElement = document.getElementById('message');
		if (!messageElement)
			return console.error('Element with class "message" not found');
		if (data.status === 'ok')
		{
			console.log('INSCRIPTION REUSSIE');
			window.location.hash = 'login';
		}
		else if (data.status === 'error')
		{
			console.log('ERREUR D\'INSCRIPTION');
			messageElement.textContent = data.message;
		}
	},

	editProfile: function(data)
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
		}
	},
};