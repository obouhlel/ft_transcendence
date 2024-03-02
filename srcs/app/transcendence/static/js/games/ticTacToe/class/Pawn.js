import * as THREE from 'three';

export class PawnCross {
    constructor(game, x, z) {
        let color = 0xff0000;
        if (game.pawnStr == 'X') {
            color = 0x0000ff;
        }
        const geometry = new THREE.BoxGeometry(1, 1, 5);
        const material = new THREE.MeshBasicMaterial({ color: color });

        const part1 = new THREE.Mesh(geometry, material);
        const part2 = new THREE.Mesh(geometry, material);

        part1.rotation.y = 15;
        part2.rotation.y = -15;

        this.cube = new THREE.Group();
        this.cube.add(part1);
        this.cube.add(part2);

        this.cube.position.x = x;
        this.cube.position.z = z;
        this.cube.position.y = 5;
        game.scene.add(this.cube);
    }
}

export class PawnCircle {
    constructor(game, x, z) {
        let color = 0xff0000;
        if (game.pawnStr == 'O') {
            color = 0x0000ff;
        }
        const geometry = new THREE.TorusGeometry(2, 0.5, 16, 100);
        const material = new THREE.MeshBasicMaterial({ color: color });
        this.cube = new THREE.Mesh(geometry, material);

        this.cube.rotation.x = Math.PI / 2;

        this.cube.position.x = x;
        this.cube.position.z = z;
        this.cube.position.y = 5;

        game.scene.add(this.cube);
    }
}