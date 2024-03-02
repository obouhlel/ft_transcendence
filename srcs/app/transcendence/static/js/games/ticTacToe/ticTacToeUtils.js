import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

import { SIZE_CASE } from './ticTacToe.js';
import * as UTILS from '../threeJsUtils.js';

import { PawnCross, PawnCircle } from './class/Pawn.js';
import { Case } from './class/Case.js';

function placeCamera(camera, mapSize) {
    camera.position.x = mapSize / 3 + 1;
    camera.position.z = mapSize / 3 + 16;
    camera.position.y = mapSize - 5;
    camera.lookAt(mapSize / 3 + 1, 0, mapSize / 3 + 1);
}

export function createCamera(renderer, mapSize) {
    let camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    placeCamera(camera, mapSize);
    return { camera };
}

function placeFloor(floor, mapSize) {
    floor.position.x = mapSize / 3;
    floor.position.z = mapSize / 3;
    floor.position.y = -0.6;
}

export function putFloor(scene, mapSize) {
    let geometry = new THREE.BoxGeometry(mapSize, 0.1, mapSize);
    let material = new THREE.MeshBasicMaterial({ color: 'grey' });
    const floor = new THREE.Mesh(geometry, material);
    placeFloor(floor, mapSize);
    UTILS.addShadowsToMesh(floor);
    scene.add(floor);
    return floor;
}

function placeTextTurn(textTurn, str) {
    if (['You win', 'You lose', 'Draw', 'Your Turn'].includes(str)) {
        textTurn.position.x = 24 / 6 + 1;
    }
    else {
        textTurn.position.x = 24 / 12 + 1;
    }
    textTurn.position.z = -11;
    textTurn.position.y = 1;
}

function createTextTurn(scene, turnString) {
    let textGeometry = UTILS.doTextGeo(turnString, 1.5);
    let meshMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
    let textTurn = new THREE.Mesh(textGeometry, meshMaterial);
    placeTextTurn(textTurn, turnString);
    scene.add(textTurn);
    return textTurn;
}

export function updateTurn(scene, turnString, game) {
    scene.remove(game.textTurn);
    game.textTurn = createTextTurn(scene, turnString);
}

export function createArena(scene) {
    const arena = [];
    for (let i = 0; i < 3; i++) {
        arena.push([]);
        for (let j = 0; j < 3; j++) {
            const x = i * SIZE_CASE + i;
            const z = j * SIZE_CASE + j;
            const name = { x: i, z: j}
            arena[i].push(new Case(scene, x, z, name));
        }
    }
    return arena;
}

export function getPawn(game) {
    let pawn = null;
    if (game.pawnStr == 'O') {
        pawn = new PawnCircle(game, 0, 0);
    } else if (game.pawnStr == 'X') {
        pawn = new PawnCross(game, 0, 0);
    }
    return pawn;
}

export function move(keys, game) {
    if (keys['ArrowUp'] == 'down' && game.previewPosition.z > 0) {
        game.previewPosition.z -= 1;
        keys['ArrowUp'] = 'done';
    }
    if (keys['ArrowDown'] == 'down' && game.previewPosition.z < game.arena.length - 1) {
        game.previewPosition.z += 1;
        keys['ArrowDown'] = 'done';
    }
    if (keys['ArrowLeft'] == 'down' && game.previewPosition.x > 0) {
        game.previewPosition.x -= 1;
        keys['ArrowLeft'] = 'done';
    }
    if (keys['ArrowRight'] == 'down' && game.previewPosition.x < game.arena.length - 1) {
        game.previewPosition.x += 1;
        keys['ArrowRight'] = 'done';
    }
}

export function printPrev(keys, game) {
    const arenaCase = game.arena[game.previewPosition.x][game.previewPosition.z];
    game.pawn.cube.position.x = arenaCase.floor.position.x;
    game.pawn.cube.position.z = arenaCase.floor.position.z;
    if (arenaCase.pawnOnThis == null && game.isMyTurn) {
        if (keys[' '] == 'down') {
            keys[' '] = 'done';
            game.isMyTurn = false;
            TIK_TAK_TOE.updateTurn(game.scene, 'Opponent turn', game);
            arenaCase.pawnOnThis = game.pawn;
            game.pawn = TIK_TAK_TOE.getPawn(game);
            sendNewPawnPosition(game, game.previewPosition.x, game.previewPosition.z); 
        }
    }
}