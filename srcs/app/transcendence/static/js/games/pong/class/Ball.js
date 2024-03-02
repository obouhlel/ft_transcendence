import * as THREE from 'three';
import * as UTILS from '../../threeJsUtils.js';

export class Ball {
    constructor(scene) {
        this.speed = 0.1;
        this.direction = new THREE.Vector3(0, 0, 0);
        this.cube = new THREE.Mesh(
            new THREE.SphereGeometry(0.4, 32, 32),
            new THREE.MeshStandardMaterial({ color: 0x00ff00 })
        );
        this.hitbox = new THREE.Box3().setFromObject(this.cube);

        this.cube.position.y = -0.2;

        UTILS.addShadowsToMesh(this.cube);
        scene.add(this.cube);
    }
}