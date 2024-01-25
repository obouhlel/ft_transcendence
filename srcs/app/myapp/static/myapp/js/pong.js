import { main } from './app.js';
import { createElt } from './utils.js';

const keyMap = {
	'ArrowUp': false,
	'ArrowDown': false,
	'z': false,
	's': false,
	'w': false,
	' ': false
};

function handleKeyDown(event)
{
	const keyDown = event.key;

	for (const key in keyMap)
		if (key === keyDown)
			keyMap[key] = true;
}

function handleKeyUp(event)
{
	const keyUp = event.key;

	for (const key in keyMap)
		if (key === keyUp)
			keyMap[key] = false;
}

export function pong()
{
	/* Arena */
	const arena = createElt('div', 'Arena');
	if (arena)
		main.appendChild(arena);

	/* Score */
	const score = createElt('div', 'Score');
	if (score)
		arena.appendChild(score);

	const scoreLeft = createElt('span', 'ScoreLeft', '0');
	if (scoreLeft)
		score.appendChild(scoreLeft);

	const scoreRight = createElt('span', 'ScoreRight', '0');
	if (scoreRight)
		score.appendChild(scoreRight);

	/* Player Left */
	const playerLeft = createElt('div', 'Player');
	playerLeft.id = 'playerLeft';
	if (playerLeft)
		arena.appendChild(playerLeft);

	/* Player Right */
	const playerRight = createElt('div', 'Player');
	playerRight.id = 'playerRight';
	if (playerRight)
		arena.appendChild(playerRight);

	/* Ball */
	const ball = createElt('div', 'Ball');
	if (ball)
		arena.appendChild(ball);

	/* Get Rect */
	const arenaRect = arena.getBoundingClientRect();
	const playerLeftRect = playerLeft.getBoundingClientRect();
	const playerRightRect = playerRight.getBoundingClientRect();
	const ballRect = ball.getBoundingClientRect();

	/* Move Player */
	function updateGame()
	{
		const speed = 5;
		const arenaTop = arena.offsetTop;
		const arenaBot = arena.offsetHeight + arena.offsetTop;
		const playerRightTop = playerRight.offsetTop;
		const playerRightBot = playerRight.offsetHeight + playerRight.offsetTop;
		const playerLeftTop = playerLeft.offsetTop;
		const playerLeftBot = playerLeft.offsetHeight + playerLeft.offsetTop;

		window.addEventListener('keydown', (event) => handleKeyDown(event));
		window.addEventListener('keyup', (event) => handleKeyUp(event));

		// Player Right
		if (keyMap['ArrowUp'] !== keyMap['ArrowDown'])
		{
			if (keyMap['ArrowUp'] && playerRightTop - speed > arenaTop)
			{
				playerRight.style.top = `${playerRight.offsetTop - speed}px`;
			}
			else if (keyMap['ArrowDown'] && playerRightBot + speed < arenaBot)
			{
				playerRight.style.top = `${playerRight.offsetTop + speed}px`;
			}
		}

		// Player Left
		if (keyMap['z'] !== keyMap['s'] || keyMap['w'] !== keyMap['s'])
		{
			if ((keyMap['z'] || keyMap['w']) && playerLeftTop - speed > arenaTop)
			{
				playerLeft.style.top = `${playerLeft.offsetTop - speed}px`;
			}
			else if (keyMap['s'] && playerLeftBot + speed < arenaBot)
			{
				playerLeft.style.top = `${playerLeft.offsetTop + speed}px`;
			}
		}

		requestAnimationFrame(updateGame);
	}

	updateGame();
}