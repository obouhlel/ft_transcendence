import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

import * as UTILS from './threeJsUtils.js';
import * as PONG from './pongUtils.js';

import * as JS_UTILS from './jsUtils.js';

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

function socketListener(socket) {
	socket.onopen = function(e) {
		console.log("Connection established");
	}
	
	socket.onmessage = function(e) {
		let data = JSON.parse(e.data);
		console.log("Received message: " + e.data);
	}
	
	socket.onclose = function(e) {
		console.log("Connection closed");
	}
	
	socket.onerror = function(error) {
		console.log(`socket error: ${event}`);
		console.error(event);
	}
}

export function pong3D() {
	const socketPath = JS_UTILS.readCookie("roomID");
	JS_UTILS.eraseCookie("roomID");
	console.log(`socketPath: ${socketPath}`);
	const url = `wss://${window.location.host}/${socketPath}`;
	const socket = new WebSocket(url);
	socketListener(socket);

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

	let lastTime = 0;
	// ------------------------------------loop------------------------------------
	function animate(currentTime) {
		if (lastTime) {
			let delta = (currentTime - lastTime) / 10;
			if (PONG.isGameGoing(game)) {
				playerLeft.move(keys, arena, delta);
				playerRight.move(keys, arena, delta);
			}
			if (PONG.isGameStarting(game)) {
				game.memGoing = true;
				ball.reset(scene, playerLeft, playerRight, button, game);
			}
			ball.move(scene, playerLeft, playerRight, button, arena, game, delta);
			PONG.lightFollowTarget(light.spot, ball.cube);
			display.controls.update();
			renderer.render(scene, display.camera);
		}
		lastTime = currentTime;
		requestAnimationFrame(animate);
	}

	animate();
}
