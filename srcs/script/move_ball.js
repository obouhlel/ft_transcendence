let ballDirection = { x: 1, y: 1 };
let ballSpeed = 1;

export const moveBall = () => {
    let ball = document.getElementById('ball');
    let main = document.querySelector('main');

    let ballRect = ball.getBoundingClientRect();
    let mainRect = main.getBoundingClientRect();

    // Vérifie si la balle a touché le joueur ou les bords de l'élément main
    if (ballRect.left <= mainRect.left || ballRect.right >= mainRect.right) {
        ballDirection.x *= -1;
    }
    if (ballRect.top <= mainRect.top || ballRect.bottom >= mainRect.bottom) {
        ballDirection.y *= -1;
    }

    // Déplace la balle
    ball.style.left = (ball.offsetLeft + ballSpeed * ballDirection.x) + 'px';
    ball.style.top = (ball.offsetTop + ballSpeed * ballDirection.y) + 'px';
}