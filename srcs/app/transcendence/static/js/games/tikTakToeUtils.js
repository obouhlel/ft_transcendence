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