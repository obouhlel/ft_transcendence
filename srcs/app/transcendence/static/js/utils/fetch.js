// export const SERVER_URL = 'https://localhost:8000';
export const SERVER_URL = '';

export const doRequest = {
    _getCookie: function getCookie(name)
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
    },

    post: function(url, data, callback)
    {
        const csrftoken = this._getCookie('csrftoken');
        const options = {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json'
            },
            credentials: 'include'
        };
        options.body = JSON.stringify(data);
        fetch(url, options)
        .then(response => response.json())
        .then(data => { callback(data); })
        .catch(error => { console.error(error); });
    },

    get: function(url) {
        const csrftoken = this._getCookie('csrftoken');
        const options = {
            method: 'GET',
            headers: {'X-CSRFToken': csrftoken},
            credentials: 'include'
        };
        return fetch(url, options)
        .then(response => response.json())
        .catch(error => { console.error(error); });
    },
};