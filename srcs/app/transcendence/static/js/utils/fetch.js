export const SERVER_URL = window.location.origin;

export function getCookie(name)
{
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break ;
            }
        }
    }
    return cookieValue;
}

export const doRequest = {
    post: async function(url, data, callback) {
        const csrftoken = getCookie('csrftoken');
        const options = {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            credentials: 'include',
        };

        if (data instanceof FormData) {
            options.body = data;
        }
        else {
            options.headers['Content-Type'] = 'application/json';
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(`${SERVER_URL}${url}`, options);
            if (response.status === 401 || response.status === 403) {
                window.location.href = '#login';
                return ;
            }
            const responseData = await response.json();
            if (callback)
                callback(responseData);
        }
        catch (error) {
            console.error("Can't do request post");
        }
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
            const response = await fetch(`${SERVER_URL}${url}`, options);
            if (!response.ok) {
                throw new Error(`Error : ${response.statusText} - ${response.status}`);
            }
            return await response.json();
        }
        catch (error) {
            return ;
            // console.error("Can't do request get");
        }
    },

    delete: async function(url, callback) {
        const csrftoken = getCookie('csrftoken');
        const options = {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            credentials: 'include',
        };
        try {
            const response = await fetch(`${SERVER_URL}${url}`, options);
            const data = await response.json();
            callback();
        }
        catch (error) {
            return ;
            // console.error("Can't do request delete");
        }
    }
};
