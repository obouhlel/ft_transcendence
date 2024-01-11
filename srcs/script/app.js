import { getElt, createElt, importCSS } from './utils.js';
import { keyMap, handleKeyDown, handleKeyUp, move } from './move_player.js';
import { moveBall } from './move_ball.js';

importCSS('./style/app.css');

const header = getElt('header');
const footer = getElt('footer');
export const main = getElt('main');

const title = createElt('h1', 'title', 'Pong');
if (title)
	header.appendChild(title);

const copy = createElt('p', 'copy', '© 2024 - All rights reserved');
if (copy)
	footer.appendChild(copy);

/* Score */

const score = createElt('div', 'Score');
if (score)
	main.appendChild(score);

export const scoreLeft = createElt('div', 'ScoreLeft', '0');
if (scoreLeft)
	score.appendChild(scoreLeft);

export const scoreRight = createElt('div', 'ScoreRight', '0');
if (scoreRight)
	score.appendChild(scoreRight);

/* Ball */

const ball = createElt('div', 'Ball');
ball.id = 'ball';
if (ball)
	main.appendChild(ball);

setInterval(moveBall, 1);

/* Players */

export const playerLeft = createElt('div', 'Player');
playerLeft.id = 'playerLeft';
if (playerLeft)
	main.appendChild(playerLeft);

export const playerRight = createElt('div', 'Player');
playerRight.id = 'playerRight';
if (playerRight)
	main.appendChild(playerRight);

window.addEventListener('keydown', (event) => handleKeyDown(event));
window.addEventListener('keyup', (event) => handleKeyUp(event));
window.addEventListener('keydown', () => move());
window.addEventListener('keyup', () => move());