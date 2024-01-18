import { main, ball, scoreLeft, scoreRight, playerLeft, playerRight } from './app.js';
import { getElt } from './utils.js';

const ballDirection = { x: 1, y: 1 };
const ballSpeed = 2;

function incrementScore(mainRect, ballRect)
{
    if (ballRect.left <= mainRect.left)
    {
        scoreRight.textContent = parseInt(scoreRight.textContent) + 1;
    }
    else if (ballRect.right >= mainRect.right)
    {
        scoreLeft.textContent = parseInt(scoreLeft.textContent) + 1;
    }
}

function collisionPlayerLeft(playerLeftRect, ballRect)
{
    if (playerLeftRect.right >= ballRect.left &&
        playerLeftRect.left <= ballRect.right &&
        playerLeftRect.bottom >= ballRect.top &&
        playerLeftRect.top <= ballRect.bottom)
    {
        return true;
    }
    return false;
}

function collisionPlayerRight(playerRightRect, ballRect) {
    if (playerRightRect.right >= ballRect.left &&
        playerRightRect.left <= ballRect.right &&
        playerRightRect.bottom >= ballRect.top &&
        playerRightRect.top <= ballRect.bottom)
    {
        return true;
    }
    return false;
}

function collisionX(main, ball, playerLeft, playerRight)
{
    const ballRect = ball.getBoundingClientRect();
    const playerLeftRect = playerLeft.getBoundingClientRect();
    const playerRightRect = playerRight.getBoundingClientRect();
    const mainRect = main.getBoundingClientRect();

    if (ballRect.left <= mainRect.left || ballRect.right >= mainRect.right)
    {
        ballDirection.x *= -1;
        incrementScore(mainRect, ballRect);
    }
    else if (collisionPlayerLeft(playerLeftRect, ballRect))
    {
        ballDirection.x *= -1;
    }
    else if (collisionPlayerRight(playerRightRect, ballRect))
    {
        ballDirection.x *= -1;
    }
}

function collisionY(main, ball)
{
    const ballRect = ball.getBoundingClientRect();
    const mainRect = main.getBoundingClientRect();

    if (ballRect.top <= mainRect.top || ballRect.bottom >= mainRect.bottom)
    {
        ballDirection.y *= -1;
    }
}

export const moveBall = () => {
    collisionX(main, ball, playerLeft, playerRight);
    collisionY(main, ball);
    ball.style.left = (ball.offsetLeft + ballSpeed * ballDirection.x) + 'px';
    ball.style.top = (ball.offsetTop + ballSpeed * ballDirection.y) + 'px';
}