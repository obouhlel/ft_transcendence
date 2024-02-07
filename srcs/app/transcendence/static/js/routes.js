// import { login } from './login.js';
// import { signin } from './signin.js';
// import { games } from './games.js';
import { game, listenerGame } from './game.js';
import { pong3D } from './pong.js';
import { shooter } from './shooter.js';

const routes = {
	'/': null,
	'/login/': null,
	'/signin/': null,
	'/games/': null,
	'/game/': game,
	'/pong/': pong3D,
	'/shooter/': shooter
};

const listeners = {
	'/': null,
	'/login/': null,
	'/signin/': null,
	'/games/': null,
	'/game/': listenerGame,
	'/pong/': null,
	'/shooter/': null
};

function route()
{
    const url = window.location.pathname;
    const routeFunc = routes[url];
    const listenerFunc = listeners[url];

	console.log(url);
	console.log(routeFunc);
	console.log(listenerFunc);
    if (routeFunc)
	{
		// Route to the function
        routeFunc();
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
