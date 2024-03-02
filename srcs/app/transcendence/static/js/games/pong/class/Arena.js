import * as THREE from 'three';
import { X_SIZE_MAP } from '../pong.js';

export class Arena {
    constructor(scene) {
        this.cube = new THREE.LineSegments(
            new THREE.EdgesGeometry(new THREE.BoxGeometry(X_SIZE_MAP, 1, 20)),
            new THREE.LineBasicMaterial({ color: 0xffffff, linewidth: 2 })
        );
        this.hitbox = new THREE.Box3().setFromObject(this.cube);

        scene.add(this.cube);
    }
}