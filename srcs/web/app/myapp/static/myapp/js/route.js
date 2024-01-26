import { home } from './home.js';
import { pong } from './pong.js';

export function route()
{
    const pathname = window.location.pathname;

	console.log(pathname);
    if (pathname === '/')
        home();
    else if (pathname === '/home/')
        home();
    else if (pathname === '/pong/')
        pong();
    else
        home();
}
