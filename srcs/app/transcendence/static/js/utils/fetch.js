export const SERVER_URL = window.location.origin;

function getCookie(name)
{
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
}

export const doRequest = {

    post: function(url, data, callback)
    {
        const csrftoken = getCookie('csrftoken');
        const options = {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            credentials: 'include',
        };
		if (data instanceof FormData)
            options.body = data;
		else
		{
			options.headers['Content-Type'] = 'application/json';
			options.body = JSON.stringify(data);
		}
        fetch(url, options)
            .then(response => response.json())
            .then(data => { callback(data); })
            .catch(error => { console.error(error); });
    },

    get: async function(url) {
        const csrftoken = getCookie('csrftoken');
        const options = {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            credentials: 'include'
        };
        try {
            const response = await fetch(url, options);
            const data = await response.json();
            if (!response.ok) {
                throw new Error(`Error : ${data.message} - ${response.status}`);
            }
            return data;
        }
        catch (error) {
            console.error(error);
        }
    },
};