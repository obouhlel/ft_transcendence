// ---------------------------------------PLAYER---------------------------------------
export function playerHitTop(player, arenaHitbox) {
    if (player.hitbox.min.z - player.speed > arenaHitbox.min.z)
        player.cube.position.z -= player.speed;
    else
        player.cube.position.z = arenaHitbox.min.z + player.size / 2;
}

export function playerHitBottom(player, arenaHitbox) {
    if (player.hitbox.max.z + player.speed < arenaHitbox.max.z)
        player.cube.position.z += player.speed;
    else
        player.cube.position.z = arenaHitbox.max.z - player.size / 2;
}

// ---------------------------------------BALL---------------------------------------
export function ballHitTopOrBot(ball, arenaHitbox) {
    if (ball.hitbox.max.z >= arenaHitbox.max.z || ball.hitbox.min.z <= arenaHitbox.min.z)
        ball.direction.z *= -1
}

export function ballHitGoal(ball, arenaHitbox) {
    if (ball.hitbox.min.x <= arenaHitbox.min.x)
        return "left";
    else if (ball.hitbox.max.x >= arenaHitbox.max.x)
        return "right";
}

export function ballHitPlayer(ball, player) {
    if (ball.hitbox.intersectsBox(player.hitbox)) {
        let newDirection = new THREE.Vector3();
        newDirection.x = ball.cube.position.x - player.cube.position.x;
        newDirection.y = 0;
        newDirection.z = ball.cube.position.z - player.cube.position.z;
        ball.direction = newDirection;
    }
}

function isBallBetwinArenaPlayerTop (ball, player, arenaHitbox) {
    if (ball.hitbox.max.z >= arenaHitbox.max.z && ball.hitbox.min.z <= player.hitbox.max.z)
        return true;
    return false;
}

function isbBallBetwinArenaPlayerBot (ball, player, arenaHitbox) {
    if (ball.hitbox.min.z <= arenaHitbox.min.z && ball.hitbox.max.z >= player.hitbox.min.z)
        return true;
    return false;
}

function isBallBehindPlayer(ball, player) {
    if (player.type == "left") {
        if ((ball.hitbox.min.x >= player.hitbox.min.x && ball.hitbox.min.x <= player.hitbox.max.x)
        || (ball.cube.position.x >= player.hitbox.min.x && ball.cube.position.x <= player.hitbox.max.x))
            return true;
    }
    else if (player.type == "right") {
        if ((ball.hitbox.max.x >= player.hitbox.min.x && ball.hitbox.max.x <= player.hitbox.max.x)
        || (ball.cube.position.x >= player.hitbox.min.x && ball.cube.position.x <= player.hitbox.max.x))
            return true;
    }
    return false;
}

export function ballPinch(ball, player, arenaHitbox) {
    if (isBallBetwinArenaPlayerTop(ball, player, arenaHitbox)
        && isBallBehindPlayer(ball, player)) {
            let newDirection = new THREE.Vector3(1, 0, -0.5);
            if (player.type == "right")
                newDirection.x *= -1;
            ball.direction = newDirection;
            ball.speed = 2;
    }
    else if (isbBallBetwinArenaPlayerBot(ball, player, arenaHitbox)
        && isBallBehindPlayer(ball, player)) {
            let newDirection = new THREE.Vector3(1, 0, 0.5);
            if (player.type == "right")
                newDirection.x *= -1;
            ball.direction = newDirection;
            ball.speed = 2;
    }
}

export function ballAntiBlockSystem(ball, player) {
    if (ball.cube.position.x == player.cube.position.x 
        && ball.hitbox.intersectsBox(player.hitbox)) {
            let newDirectionX = 0.2;
            if (player.type == "right")
                newDirectionX *= -1;
            ball.direction.x = newDirectionX;
    }
}
