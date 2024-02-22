import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

import * as UTILS from './threeJsUtils.js';

// ---------------------------------------PLAYER---------------------------------------
function isPlayerHitTop(player, arenaHitbox) {
    return player.hitbox.min.z - player.speed > arenaHitbox.min.z;
}

function isPlayerHitBot(player, arenaHitbox) {
    return player.hitbox.max.z + player.speed < arenaHitbox.max.z;
}

export function playerMoveTop(player, arenaHitbox) {
    if (isPlayerHitTop(player, arenaHitbox)) player.cube.position.z -= player.speed;
    else player.cube.position.z = arenaHitbox.min.z + player.size / 2;
}

export function playerMoveBottom(player, arenaHitbox) {
    if (isPlayerHitBot(player, arenaHitbox)) player.cube.position.z += player.speed;
    else player.cube.position.z = arenaHitbox.max.z - player.size / 2;
}

export function playerReset(player) {
    player.cube.position.z = 0;
}

// ---------------------------------------BALL---------------------------------------
export function ballHitTopOrBot(ball, arenaHitbox) {
    if (ball.hitbox.max.z >= arenaHitbox.max.z || ball.hitbox.min.z <= arenaHitbox.min.z) ball.direction.z *= -1;
}

export function ballHitGoal(ball, arenaHitbox) {
    if (ball.hitbox.min.x <= arenaHitbox.min.x) return 'left';
    else if (ball.hitbox.max.x >= arenaHitbox.max.x) return 'right';
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

function isBallBetwinArenaPlayerTop(ball, player, arenaHitbox) {
    if (ball.hitbox.max.z >= arenaHitbox.max.z && ball.hitbox.min.z <= player.hitbox.max.z) return true;
    return false;
}

function isbBallBetwinArenaPlayerBot(ball, player, arenaHitbox) {
    if (ball.hitbox.min.z <= arenaHitbox.min.z && ball.hitbox.max.z >= player.hitbox.min.z) return true;
    return false;
}

function isBallBehindPlayer(ball, player) {
    if (player.type == 'left') {
        if (
            (ball.hitbox.min.x >= player.hitbox.min.x && ball.hitbox.min.x <= player.hitbox.max.x) ||
            (ball.cube.position.x >= player.hitbox.min.x && ball.cube.position.x <= player.hitbox.max.x)
        )
            return true;
    } else if (player.type == 'right') {
        if (
            (ball.hitbox.max.x >= player.hitbox.min.x && ball.hitbox.max.x <= player.hitbox.max.x) ||
            (ball.cube.position.x >= player.hitbox.min.x && ball.cube.position.x <= player.hitbox.max.x)
        )
            return true;
    }
    return false;
}

export function ballPinch(ball, player, arenaHitbox) {
    if (isBallBetwinArenaPlayerTop(ball, player, arenaHitbox) && isBallBehindPlayer(ball, player)) {
        let newDirection = new THREE.Vector3(1, 0, -0.5);
        if (player.type == 'right') newDirection.x *= -1;
        ball.direction = newDirection;
        ball.speed = 2;
    } else if (isbBallBetwinArenaPlayerBot(ball, player, arenaHitbox) && isBallBehindPlayer(ball, player)) {
        let newDirection = new THREE.Vector3(1, 0, 0.5);
        if (player.type == 'right') newDirection.x *= -1;
        ball.direction = newDirection;
        ball.speed = 2;
    }
}

export function ballSlowSystem(ball) {
    if (ball.speed > 0.1) ball.speed -= 0.1;
}

export function ballAntiBlockSystem(ball, player) {
    if (ball.cube.position.x == player.cube.position.x && ball.hitbox.intersectsBox(player.hitbox)) {
        let newDirectionX = 0.2;
        if (player.type == 'right') newDirectionX *= -1;
        ball.direction.x = newDirectionX;
    }
}

export function ballReset(ball) {
    ball.cube.position.x = 0;
    ball.cube.position.z = 0;
    ball.direction.set(0, 0, 0);
}

// ---------------------------------------UTILS---------------------------------------
function placeTitle(title) {
    title.position.x = -9;
    title.position.z = -17;
    title.position.y = 1.16;
    title.rotation.x = -0.7;
}

export function putTitle(scene) {
    let textGeometry = UTILS.doTextGeo('PONG', 5, true);
    let meshMaterial = new THREE.MeshStandardMaterial({ color: 0xffffff });
    const title = new THREE.Mesh(textGeometry, meshMaterial);
    placeTitle(title);
    scene.add(title);
}

function placeFloor(floor) {
    floor.position.y = -0.6;
}

export function putFloor(scene, mapSize) {
    let geometry = new THREE.BoxGeometry(mapSize, 0.1, 20);
    let material = new THREE.MeshStandardMaterial({ color: 0xffffff });
    const floor = new THREE.Mesh(geometry, material);
    placeFloor(floor);
    UTILS.addShadowsToMesh(floor);
    scene.add(floor);
}

function placeCamera(camera, mapSize) {
    camera.position.z = 10;
    camera.position.y = mapSize - 5;
}

function setupControls(controls) {
    controls.enableRotate = true;
    controls.rotateSpeed = 1;
    controls.target.set(0, 0, 0);
}

export function createCamera(renderer, mapSize) {
    let camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    placeCamera(camera, mapSize);
    let controls = new OrbitControls(camera, renderer.domElement);
    setupControls(controls);
    return { camera: camera, controls: controls };
}

function placeTextScore(textScore) {
    textScore.position.x = -2;
    textScore.position.z = -11;
    textScore.position.y = 1;
}

function createTextScore(scene, scoreString) {
    let textGeometry = UTILS.doTextGeo(scoreString, 1.5);
    let meshMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
    let textScore = new THREE.Mesh(textGeometry, meshMaterial);
    placeTextScore(textScore);
    scene.add(textScore);
    return textScore;
}

export function updateScore(scene, scoreString, game) {
    scene.remove(game.textScore);
    game.textScore = createTextScore(scene, scoreString);
}

function placeLight(spot, globalLight, mapSize) {
    spot.position.set(0, mapSize / 2, 0);
    globalLight.position.set(0, 10, 20);
    globalLight.shadow.camera.left = -(mapSize / 2);
    globalLight.shadow.camera.right = mapSize / 2;
    globalLight.shadow.camera.top = 10;
    globalLight.shadow.camera.bottom = -10;
    globalLight.shadow.camera.near = 0.5;
    globalLight.shadow.camera.far = 500;
}

export function createLight(scene, mapSize) {
    const spot = new THREE.SpotLight(0xffffff, 50, 100, Math.PI / 8, 0);
    const globalLight = new THREE.DirectionalLight(0xffffff, 1);

    globalLight.castShadow = true;
    spot.castShadow = true;
    placeLight(spot, globalLight, mapSize);
    scene.add(spot);
    scene.add(spot.target);
    scene.add(globalLight);
    return { spot: spot, globalLight: globalLight };
}

export function isGameStarting(game) {
    return game.going && !game.memGoing;
}

export function isGameGoing(game) {
    return game.going;
}

export function lightFollowTarget(light, ball) {
    let spotTarget = new THREE.Vector3();
    spotTarget.set(ball.position.x, ball.position.y, ball.position.z);
    light.target.position.copy(spotTarget);
}
