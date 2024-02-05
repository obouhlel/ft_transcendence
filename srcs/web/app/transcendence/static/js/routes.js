// import { login } from './login.js';
// import { signin } from './signin.js';
// import { games } from './games.js';
import { pong3D } from './pong.js';
// import { pew } from './pew.js';

const routes = {
	'/': null,
	'/login': null,
	'/signin': null,
	'/games': null,
	'/pong': pong3D,
	'/pew': null
};

const listeners = {
	'/': null,
	'/login': null,
	'/signin': null,
	'/games': null,
	'/pong': null,
	'/pew': null
};

function route()
{
    const url = window.location.pathname;
    const routeFunc = routes[url];
    const listenerFunc = listeners[url];

    if (routeFunc)
	{
		// Route to the function
        func();
    }
	// else
	// {
	// 	// Default route
    //     login();
    // }

    if (listenerFunc)
	{
		// Call the listener function
        listenerFunc();
    }
}

window.addEventListener('popstate', route);
route();
