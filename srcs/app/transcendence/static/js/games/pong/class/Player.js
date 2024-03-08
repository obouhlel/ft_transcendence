import * as THREE from 'three';
import * as PONG from '../pongUtils.js';
import * as UTILS from '../../threeJsUtils.js';

import { X_SIZE_MAP } from '../pong.js';

export class Player {
    constructor(playerType, scene, game) {
        this.type = playerType;
        this.speed = 0.1;
        this.size = 2;
        this.score = 0;
        this.keys = {
            up: '',
            down: '',
        };
        let color = { color: 0xff0000 };
        if (playerType == game.side) {
            color = { color: 0x0000ff };
            this.keys = {
                up: 'ArrowUp',
                down: 'ArrowDown',
            };
        }
        this.cube = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.5, this.size), new THREE.MeshStandardMaterial(color));
        this.hitbox = new THREE.Box3().setFromObject(this.cube);

        if (playerType == 'left') {
            this.cube.position.x = -(X_SIZE_MAP / 2) + 1;
        } else if (playerType == 'right') {
            this.cube.position.x = X_SIZE_MAP / 2 - 1;
        }

        this.cube.position.y = -0.3;

        UTILS.addShadowsToMesh(this.cube);
        scene.add(this.cube);
    }

    move(keys, arena, deltaTime) {
        this.hitbox.setFromObject(this.cube);
        this.speed = 0.1 * deltaTime;
        if (keys[this.keys['up']]) {
            PONG.playerMoveTop(this, arena.hitbox);
        }
        if (keys[this.keys['down']]) {
            PONG.playerMoveBottom(this, arena.hitbox);
        }
    }

    reset() {
        PONG.playerReset(this);
    }
}