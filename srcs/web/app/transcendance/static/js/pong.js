import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

import * as UTILS from './threeJsUtils.js';

const X_SIZE_MAP = 20;

// ------------------------------------classes------------------------------------
class Arena {
	constructor(scene) {
		this.cube = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(X_SIZE_MAP, 1, 20)), new THREE.LineBasicMaterial({ color: 0xffffff, linewidth: 2 }));
		this.hitbox = new THREE.Box3().setFromObject(this.cube);

		// this.cube.castShadow = true;
		// this.cube.receiveShadow = true;

		scene.add(this.cube);
	}
}

class Player {
	constructor(playerType, scene) {
		this.type = playerType;
		this.speed = 0.1;
		this.cube = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.5, 2), new THREE.MeshStandardMaterial({ color: 0xff0000 }));
		this.hitbox = new THREE.Box3().setFromObject(this.cube);
		this.score = 0;

		if (playerType == "left") {
			this.cube.position.x = -(X_SIZE_MAP / 2) + 1;
		} else if (playerType == "right") {
			this.cube.position.x = X_SIZE_MAP / 2 - 1;
		}
		this.cube.position.y = -0.3;

		this.cube.castShadow = true;
		this.cube.receiveShadow = true;

		scene.add(this.cube);
	}

	move(keys, arena) {
		this.hitbox.setFromObject(this.cube);
		if (this.type == "left") {
			if (keys['w']) {
				if (this.hitbox.min.z - this.speed > arena.hitbox.min.z) {
					this.cube.position.z -= this.speed;
				} else {
					this.cube.position.z = arena.hitbox.min.z + 1;
				}
			}
			if (keys['s']) {
				if (this.hitbox.max.z + this.speed < arena.hitbox.max.z) {
					this.cube.position.z += this.speed;
				} else {
					this.cube.position.z = arena.hitbox.max.z - 1;
				}
			}
		} else if (this.type == "right") {
			if (keys['ArrowUp']) {
				if (this.hitbox.min.z - this.speed > arena.hitbox.min.z) {
					this.cube.position.z -= this.speed;
				} else {
					this.cube.position.z = arena.hitbox.min.z + 1;
				}
			}
			if (keys['ArrowDown']) {
				if (this.hitbox.max.z + this.speed < arena.hitbox.max.z) {
					this.cube.position.z += this.speed;
				} else {
					this.cube.position.z = arena.hitbox.max.z - 1;
				}
			}
		}
	}

	reset() {
		this.cube.position.z = 0;
	}
}

class Ball {
	constructor(scene) {
		this.speed = 0.1;
		this.direction = new THREE.Vector3(Math.round(Math.random()) * 2 - 1, 0, 0);
		this.cube = new THREE.Mesh(new THREE.SphereGeometry(0.4, 32, 32), new THREE.MeshStandardMaterial({ color: 0x00ff00 }));
		this.hitbox = new THREE.Box3().setFromObject(this.cube);

		this.cube.position.y = -0.2;

		this.cube.castShadow = true;
		this.cube.receiveShadow = true;
		scene.add(this.cube);
	}

	move(scene, playerLeft, playerRight, button, arena) {

		// After pinch (slow systeme)
		if (this.speed > 0.1) {
			this.speed -= 0.1;
		}

		// If the ball hit the bottom or top
		this.hitbox.setFromObject(this.cube);
		arena.hitbox.setFromObject(arena.cube);
		if (this.hitbox.max.z >= arena.hitbox.max.z || this.hitbox.min.z <= arena.hitbox.min.z) {
			this.direction.z *= -1
		}

		// If the ball go through the player line (scoring)
		if (this.cube.position.x >= X_SIZE_MAP / 2) {
			playerLeft.score += 1;
			this.reset(scene, playerLeft, playerRight, button);
		} else if (this.cube.position.x <= -(X_SIZE_MAP / 2)) {
			playerRight.score += 1;
			this.reset(scene, playerLeft, playerRight, button);
		}

		// If the ball hit the player (bounce)
		playerLeft.hitbox.setFromObject(playerLeft.cube);
		playerRight.hitbox.setFromObject(playerRight.cube);
		if (this.hitbox.intersectsBox(playerLeft.hitbox)) {
			this.direction = new THREE.Vector3(this.cube.position.x - playerLeft.cube.position.x, 0, this.cube.position.z - playerLeft.cube.position.z);
		} else if (this.hitbox.intersectsBox(playerRight.hitbox)) {
			this.direction = new THREE.Vector3(this.cube.position.x - playerRight.cube.position.x, 0, this.cube.position.z - playerRight.cube.position.z);
		}

		// Pinch
		if (this.hitbox.max.z >= arena.hitbox.max.z && this.hitbox.min.z <= playerLeft.hitbox.max.z
			&& ((this.hitbox.min.x >= playerLeft.hitbox.min.x && this.hitbox.min.x <= playerLeft.hitbox.max.x)
				|| (this.cube.position.x >= playerLeft.hitbox.min.x && this.cube.position.x <= playerLeft.hitbox.max.x))) {
			this.direction = new THREE.Vector3(1, 0, -0.5);
			this.speed = 2;
		} else if (this.hitbox.max.z >= arena.hitbox.max.z && this.hitbox.min.z <= playerRight.hitbox.max.z
			&& ((this.hitbox.max.x >= playerRight.hitbox.min.x && this.hitbox.max.x <= playerRight.hitbox.max.x)
				|| (this.cube.position.x >= playerRight.hitbox.min.x && this.cube.position.x <= playerRight.hitbox.max.x))) {
			this.direction = new THREE.Vector3(-1, 0, -0.5);
			this.speed = 2;
		}
		if (this.hitbox.min.z <= arena.hitbox.min.z && this.hitbox.max.z >= playerLeft.hitbox.min.z
			&& ((this.hitbox.min.x >= playerLeft.hitbox.min.x && this.hitbox.min.x <= playerLeft.hitbox.max.x)
				|| (this.cube.position.x >= playerLeft.hitbox.min.x && this.cube.position.x <= playerLeft.hitbox.max.x))) {
			this.direction = new THREE.Vector3(1, 0, 0.5);
			this.speed = 2;
		} else if (this.hitbox.min.z <= arena.hitbox.min.z && this.hitbox.max.z >= playerRight.hitbox.min.z
			&& ((this.hitbox.max.x >= playerRight.hitbox.min.x && this.hitbox.max.x <= playerRight.hitbox.max.x)
				|| (this.cube.position.x >= playerRight.hitbox.min.x && this.cube.position.x <= playerRight.hitbox.max.x))) {
			this.direction = new THREE.Vector3(-1, 0, 0.5);
			this.speed = 2;
		}

		// AntiBlock system
		if (this.cube.position.x == playerLeft.cube.position.x && this.hitbox.intersectsBox(playerLeft.hitbox)) {
			this.direction.x = -0.2;
		} else if (this.cube.position.x == playerRight.cube.position.x && this.hitbox.intersectsBox(playerRight.hitbox)) {
			this.direction.x = 0.2;
		}

		// Setup the director vector
		this.direction.normalize();
		this.direction.multiplyScalar(this.speed);
		this.cube.position.add(this.direction);
	}

	reset(scene, playerLeft, playerRight, button) {
		updateScore(scene, playerLeft, playerRight, button);
		this.cube.position.x = 0;
		this.cube.position.z = 0;
		this.direction.set(Math.round(Math.random()) * 2 - 1, 0, 0);
		playerLeft.reset();
		playerRight.reset();
	}
}

let textScore = new THREE.Mesh(UTILS.doTextGeo("0 - 0", 1.5), new THREE.MeshBasicMaterial({ color: 0xffffff }));

function updateScore(scene, playerLeft, playerRight, button) {
	if (scene && textScore) {
		// If the TextScore already exist, remove it
		scene.remove(textScore);
	}

	if (playerLeft.score == 10 || playerRight.score == 10) {
		// End of the game
		button.innerHTML = "RESTART";
		button.style.display = "block";
		going = false;
		memGoing = false;
	}
	let scoreString = playerLeft.score.toString() + " - " + playerRight.score.toString();
	textScore = new THREE.Mesh(UTILS.doTextGeo(scoreString, 1.5), new THREE.MeshBasicMaterial({ color: 0xffffff }));

	// Add to the scene and set positions
	textScore.position.x = -2;
	textScore.position.z = -11;
	textScore.position.y = 1;
	scene.add(textScore);
}


// ------------------------------------setup------------------------------------
export function pong3D() {

	let going = false;
	let memGoing = false;

	const scene = UTILS.createScene();
	const renderer = UTILS.createRenderer();
	const button = UTILS.createContainerForGame("pong", renderer);
	button.addEventListener("click", () => {
		going = true;
		button.style.display = "none";
		playerLeft.score = 0;
		playerRight.score = 0;
	});

	// 3d Title
	const title = new THREE.Mesh(UTILS.doTextGeo("PONG", 5, true), new THREE.MeshStandardMaterial({ color: 0xffffff }));

	title.position.x = -9;
	title.position.z = -17;
	title.position.y = 1.16;
	title.rotation.x = -0.7;

	scene.add(title);

	// Floor
	const floor = new THREE.Mesh(new THREE.BoxGeometry(X_SIZE_MAP, 0.1, 20), new THREE.MeshStandardMaterial({ color: 0xffffff }));

	floor.position.y = -0.6;
	floor.receiveShadow = true;
	floor.castShadow = true;
	scene.add(floor);

	// Camera
	const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
	camera.position.z = 10;
	camera.position.y = X_SIZE_MAP - 5;

	let controls = new OrbitControls(camera, renderer.domElement);
	controls.enableRotate = true;
	controls.rotateSpeed = 1.0;
	controls.target.set(0, 0, 0);

	// ------------------------------------blocks------------------------------------
	const arena = new Arena(scene);
	const ball = new Ball(scene);
	const playerLeft = new Player("left", scene);
	const playerRight = new Player("right", scene);

	// ------------------------------------light------------------------------------
	// Spot light that follow the ball
	const spot = new THREE.SpotLight(0xffffff, 50, 100, Math.PI / 8, 0);
	// Directional light that enlighte all the elements
	const globalLight = new THREE.DirectionalLight(0xffffff, 1);
	// Setup the position of both light
	spot.position.set(0, X_SIZE_MAP / 2, 0);
	globalLight.position.set(0, 10, 20);

	// Enable shadow casting
	globalLight.castShadow = true;
	spot.castShadow = true;

	// Setup the light data and fov
	globalLight.shadow.camera.left = -(X_SIZE_MAP / 2);
	globalLight.shadow.camera.right = X_SIZE_MAP / 2;
	globalLight.shadow.camera.top = 10;
	globalLight.shadow.camera.bottom = -10;
	globalLight.shadow.camera.near = 0.5;
	globalLight.shadow.camera.far = 500;

	scene.add(spot);
	scene.add(spot.target);
	scene.add(globalLight);
	updateScore(scene, playerLeft, playerRight, button);

	// ------------------------------------keys------------------------------------
	let keys = {};
	document.addEventListener('keydown', (e) => keys[e.key] = true);
	document.addEventListener('keyup', (e) => keys[e.key] = false);

	// ------------------------------------functions------------------------------------

	// To delete (cheats for debug)
	function debug() {
		if (keys['r']) {
			playerLeft.score = 0;
			playerRight.score = 0;
			ball.reset(scene, playerLeft, playerRight, button);
		}
		if (keys['4']) {
			ball.direction.x = 0;
			ball.direction.z = 0;
			ball.direction.y = 0;
			ball.cube.position.x = playerLeft.cube.position.x;
			ball.cube.position.z = playerLeft.cube.position.z + 2;
		}
		if (keys['5']) {
			ball.direction.x = 0;
			ball.direction.z = 0;
			ball.direction.y = 0;
			ball.cube.position.x = playerRight.cube.position.x;
			ball.cube.position.z = playerRight.cube.position.z + 2;
		}
		if (keys['1']) {
			ball.direction.x = 0;
			ball.direction.z = 0;
			ball.direction.y = 0;
			ball.cube.position.x = playerLeft.cube.position.x;
			ball.cube.position.z = playerLeft.cube.position.z - 2;
		}
		if (keys['2']) {
			ball.direction.x = 0;
			ball.direction.z = 0;
			ball.direction.y = 0;
			ball.cube.position.x = playerRight.cube.position.x;
			ball.cube.position.z = playerRight.cube.position.z - 2;
		}
	}

	// ------------------------------------loop------------------------------------
	function animate() {
		requestAnimationFrame(animate);

		if (going) {
			playerLeft.move(keys, arena);
			playerRight.move(keys, arena);
		}
		if (going && !memGoing) {
			memGoing = true;
			ball.reset(scene, playerLeft, playerRight, button);
		}

		ball.move(scene, playerLeft, playerRight, button, arena);
		spot.target.position.set(ball.cube.position.x, ball.cube.position.y, ball.cube.position.z);
		debug();

		controls.update();

		renderer.render(scene, camera);
	}

	animate();
}