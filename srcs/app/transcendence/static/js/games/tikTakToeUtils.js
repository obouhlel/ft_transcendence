import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

import * as UTILS from './threeJsUtils.js';

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
    if (str == 'Your turn' || str == 'You win' || str == 'You lose' || str == 'Draw') {
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