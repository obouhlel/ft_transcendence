// import { games } from './games.js';
import { game } from './game.js';
import { pong3D } from './pong.js';
import { shooter } from './shooter.js';

const routes = {
	'/': null,
	'/games/': null,
	'/game/': game,
	'/pong/': pong3D,
	'/shooter/': shooter
};

const listeners = {
	'/': null,
	'/games/': null,
	'/game/': null,
	'/pong/': null,
	'/shooter/': null
};

function defaultRoute() {}
function defaultListener() {}

function route()
{
    const url = window.location.pathname;
    const routeFunc = routes[url];
    const listenerFunc = listeners[url];

	// console.log(url);
	// console.log(routeFunc);
	// console.log(listenerFunc);

    if (routeFunc)
		routeFunc();
	else
		defaultRoute();

    if (listenerFunc)
        listenerFunc();
	else
		defaultListener();
}

window.addEventListener('popstate', route);
route();
