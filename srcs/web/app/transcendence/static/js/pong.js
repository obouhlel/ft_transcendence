import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

import * as UTILS from './threeJsUtils.js';
import * as PONG from './pongUtils.js';

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
		this.size = 2;
		this.cube = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.5, this.size), new THREE.MeshStandardMaterial({ color: 0xff0000 }));
		this.hitbox = new THREE.Box3().setFromObject(this.cube);
		this.score = 0;
		this.keys = {
			up: "",
			down: "",
		};

		if (playerType == "left") {
			this.keys = { up: "w", down: "s" };
			this.cube.position.x = -(X_SIZE_MAP / 2) + 1;
		} else if (playerType == "right") {
			this.keys = { up: "ArrowUp", down: "ArrowDown" };
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

class Ball {
	constructor(scene) {
		this.speed = 0.1;
		this.direction = new THREE.Vector3(Math.round(Math.random()) * 2 - 1, 0, 0);
		this.cube = new THREE.Mesh(new THREE.SphereGeometry(0.4, 32, 32), new THREE.MeshStandardMaterial({ color: 0x00ff00 }));
		this.hitbox = new THREE.Box3().setFromObject(this.cube);

		this.cube.position.y = -0.2;

		UTILS.addShadowsToMesh(this.cube);
		scene.add(this.cube);
	}

	move(scene, playerLeft, playerRight, button, arena, game, deltaTime) {

		PONG.ballSlowSystem(this);

		this.hitbox.setFromObject(this.cube);
		PONG.ballHitTopOrBot(this, arena.hitbox);

		if (PONG.ballHitGoal(this, arena.hitbox) == "left") {
			playerLeft.score += 1;
			this.reset(scene, playerLeft, playerRight, button, game);
		} else if (PONG.ballHitGoal(this, arena.hitbox) == "right") {
			playerRight.score += 1;
			this.reset(scene, playerLeft, playerRight, button, game);
		}

		playerLeft.hitbox.setFromObject(playerLeft.cube);
		playerRight.hitbox.setFromObject(playerRight.cube);
		PONG.ballHitPlayer(this, playerLeft);
		PONG.ballHitPlayer(this, playerRight);

		PONG.ballPinch(this, playerLeft, arena.hitbox);
		PONG.ballPinch(this, playerRight, arena.hitbox);

		PONG.ballAntiBlockSystem(this, playerLeft);
		PONG.ballAntiBlockSystem(this, playerRight);

		// Setup the director vector
		this.direction.normalize();
		this.direction.multiplyScalar(this.speed * deltaTime);
		this.cube.position.add(this.direction);
	}

	reset(scene, playerLeft, playerRight, button, game) {
		PONG.updateScore(scene, playerLeft, playerRight, button, game);
		PONG.ballReset(this);
		playerLeft.reset();
		playerRight.reset();
	}
}

export function pong3D() {
	// ------------------------------------setup------------------------------------
	let game = {
		going: false, 
		memGoing: false,
		textScore: null
	};

	const scene = UTILS.createScene();
	const renderer = UTILS.createRenderer();
	PONG.putTitle(scene);
	PONG.putFloor(scene, X_SIZE_MAP);

	let display = PONG.createCamera(renderer, X_SIZE_MAP);
	const arena = new Arena(scene);
	const ball = new Ball(scene);
	const playerLeft = new Player("left", scene);
	const playerRight = new Player("right", scene);

	const button = UTILS.createContainerForGame("pong", renderer);
	button.addEventListener("click", () => {
		game.going = true;
		button.style.display = "none";
		playerLeft.score = 0;
		playerRight.score = 0;
	});

	const light = PONG.createLight(scene, X_SIZE_MAP);
	PONG.updateScore(scene, playerLeft, playerRight, button, game);

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
			ball.reset(scene, playerLeft, playerRight, button, game);
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

	let lastTime = 0;
	// ------------------------------------loop------------------------------------
	function animate(currentTime) {
		if (lastTime) {
			let delta = (currentTime - lastTime) / 10;
			if (game.going) {
				playerLeft.move(keys, arena, delta);
				playerRight.move(keys, arena, delta);
			}
			if (game.going && !game.memGoing) {
				game.memGoing = true;
				ball.reset(scene, playerLeft, playerRight, button, game);
			}

			ball.move(scene, playerLeft, playerRight, button, arena, game, delta);
			light.spot.target.position.set(ball.cube.position.x, ball.cube.position.y, ball.cube.position.z);
			debug();

			display.controls.update();
			renderer.render(scene, display.camera);
		}
		lastTime = currentTime;
		requestAnimationFrame(animate);
	}

	animate();
}
