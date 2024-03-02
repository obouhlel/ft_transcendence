import * as THREE from 'three';

import { SIZE_CASE } from '../ticTacToe.js';
import * as TIK_TAK_TOE from '../ticTacToeUtils.js';

export class Case {
    constructor(scene, x, z, name) {
        this.cube = new THREE.LineSegments(
            new THREE.EdgesGeometry(new THREE.BoxGeometry(SIZE_CASE, 1, SIZE_CASE)),
            new THREE.LineBasicMaterial({ color: 0xffffff, linewidth: 2 })
        );
        this.cube.position.x = x;
        this.cube.position.z = z;

        this.floor = TIK_TAK_TOE.putFloor(scene, SIZE_CASE);
        this.floor.position.x = x;
        this.floor.position.z = z;
        this.floor.userData.name = name;
        this.floor.userData.clickable = true;

        this.pawnOnThis = null;
            
        scene.add(this.cube);
        scene.add(this.floor);
    }

    getPawnDown() {
        if (this.pawnOnThis != null && this.pawnOnThis.cube.position.y > 0) {
            this.pawnOnThis.cube.position.y -= 0.1;
        }
    }
}