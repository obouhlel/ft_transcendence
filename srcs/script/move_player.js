import { main, playerLeft, playerRight } from './app.js';
import { updateElt } from './utils.js';

export const keyMap = {
	'ArrowUp': false,
	'ArrowDown': false,
	'z': false,
	's': false,
	'w': false,
	' ': false
};

export function handleKeyDown(event)
{
	const keyDown = event.key;

	for (const key in keyMap)
		if (key === keyDown)
			keyMap[key] = true;
}

export function handleKeyUp(event)
{
	const keyUp = event.key;

	for (const key in keyMap)
		if (key === keyUp)
			keyMap[key] = false;
}

export function move()
{
	const mainRect = main.getBoundingClientRect();
	const playerLeftRect = playerLeft.getBoundingClientRect();
	const playerRightRect = playerRight.getBoundingClientRect();

	// If the key is pressed at the same time
	if (keyMap['ArrowUp'] && keyMap['ArrowUp'] === keyMap['ArrowDown'])
		return ;
	if (keyMap['s'] && keyMap['s'] === (keyMap['z'] || keyMap['w']))
		return ;

	// Player Left
	if (keyMap['ArrowUp'] && (playerLeftRect.top - 10) > mainRect.top)
	{
		playerLeft.style.top = `${playerLeft.offsetTop - 10}px`;
	}
	else if (keyMap['ArrowDown'] && (playerLeftRect.bottom + 10) < mainRect.bottom)
	{
		playerLeft.style.top = `${playerLeft.offsetTop + 10}px`;
	}

	// Player Right
	if ((keyMap['z'] || keyMap['w']) && (playerRightRect.top - 10) > mainRect.top)
	{
		playerRight.style.top = `${playerRight.offsetTop - 10}px`;
	}
	else if (keyMap['s'] && (playerRightRect.bottom + 10) < mainRect.bottom)
	{
		playerRight.style.top = `${playerRight.offsetTop + 10}px`;
	}
}