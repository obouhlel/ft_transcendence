export const callback = {
	login: function(data)
	{
		let messageElement = document.getElementById('message');
		if (!messageElement)
			return console.error('Element with class "message" not found');
		if (data.status === 'ok')
		{
			window.location.hash = 'games';
		}
		else if (data.status === 'error')
		{
			messageElement.textContent = data.message;
		}
	},

	logout: function(data)
	{
		if (data.status === 'ok')
		{
			window.location.hash = 'login';
		}
	},

	registered: function(data)
	{
		let messageElement = document.getElementById('message');
		if (!messageElement)
			return console.error('Element with class "message" not found');
		if (data.status === 'ok')
		{
			window.location.hash = 'login';
		}
		else if (data.status === 'error')
		{
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
			window.location.hash = 'profile';
		}
		else if (data.status === 'error')
		{
			messageElement.textContent = data.message;
		}
	},
};