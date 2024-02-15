import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

import * as UTILS from './threeJsUtils.js';
import * as PONG from './pongUtils.js';

import * as JS_UTILS from './jsUtils.js';

const X_SIZE_MAP = 20;

let username = JS_UTILS.readCookie("username");
JS_UTILS.eraseCookie("username");
let side = "not assigned";

let enemyPosition = 0;

const socketPath = JS_UTILS.readCookie("url");
JS_UTILS.eraseCookie("url");
let socket;
if (socketPath != undefined) {
	const url = `wss://${window.location.host}/${socketPath}`;
	socket = new WebSocket(url);
	socketListener(socket);
}

function sendPlayerPosition(player) {
	JS_UTILS.sendMessageToSocket(socket, { "game": "position", "username": username, "position": player.cube.position.z });
}

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
		this.score = 0;
		this.keys = {
			up: "",
			down: "",
		};
		let color = { color: 0xff0000 };
		if (playerType == side) {
			color = { color: 0x0000ff };
			this.keys = {
				up: "ArrowUp",
				down: "ArrowDown",
			};
		}
		this.cube = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.5, this.size), new THREE.MeshStandardMaterial(color));
		this.hitbox = new THREE.Box3().setFromObject(this.cube);

		if (playerType == "left") {
			this.cube.position.x = -(X_SIZE_MAP / 2) + 1;
		} else if (playerType == "right") {
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

	move(scene, playerLocal, playerSocket, arena, game, deltaTime) {

		PONG.ballSlowSystem(this);

		this.hitbox.setFromObject(this.cube);
		PONG.ballHitTopOrBot(this, arena.hitbox);

		if (PONG.ballHitGoal(this, arena.hitbox) == "left") {
			playerLocal.score += 1;
			this.reset(scene, playerLocal, playerSocket, game);
		} else if (PONG.ballHitGoal(this, arena.hitbox) == "right") {
			playerSocket.score += 1;
			this.reset(scene, playerLocal, playerSocket, game);
		}

		playerLocal.hitbox.setFromObject(playerLocal.cube);
		playerSocket.hitbox.setFromObject(playerSocket.cube);
		PONG.ballHitPlayer(this, playerLocal);
		PONG.ballHitPlayer(this, playerSocket);

		PONG.ballPinch(this, playerLocal, arena.hitbox);
		PONG.ballPinch(this, playerSocket, arena.hitbox);

		PONG.ballAntiBlockSystem(this, playerLocal);
		PONG.ballAntiBlockSystem(this, playerSocket);

		// Setup the director vector
		this.direction.normalize();
		this.direction.multiplyScalar(this.speed * deltaTime);
		this.cube.position.add(this.direction);
	}

	reset(scene, playerLocal, playerSocket, game) {
		PONG.updateScore(scene, playerLocal, playerSocket, game);
		PONG.ballReset(this);
		playerLocal.reset();
		playerSocket.reset();
	}
}

function parseMessage(message) {
	if ('game' in message) {
		if (message['game'] == "starting") {
			side = message['side'];
			getSide(socket);
		}
		if (message['game'] == "position") {
			enemyPosition = message['position'];
		}
	}
}

async function getSide(socket) {
	const timeToSleep = 1000;
	while (side == "not assigned") {
		await new Promise(r => setTimeout(r, timeToSleep));
		JS_UTILS.sendMessageToSocket(socket, { "game": "starting", "username": username });
	}
}

function socketListener(socket) {
	socket.onopen = function (e) {
		console.log("Connection established");
	}

	socket.onmessage = function (e) {
		let data = JSON.parse(e.data);
		console.log("Received message: " + e.data);
		parseMessage(data);
	}

	socket.onclose = function (e) {
		console.log("Connection closed");
	}

	socket.onerror = function (error) {
		console.log(`socket error: ${event}`);
		console.error(event);
	}

	window.addEventListener("beforeunload", function() {
		JS_UTILS.sendMessageToSocket(socket, { "game": "leaved", "username": username });
		socket.close();
	});
}

export function pong3D() {
	let socketOpen = new Promise(resolve => {
		socket.addEventListener("open", function (event) {
			resolve();
		});
	});
	socketOpen.then(() => {
		JS_UTILS.sendMessageToSocket(socket, { "game": "starting", "username": username });
	});

	let game = {
		going: false,
		memGoing: false,
		textScore: null
	};

	const scene = UTILS.createScene();
	const renderer = UTILS.createRenderer();
	UTILS.createContainerForGame("pong", renderer);
	PONG.putTitle(scene);
	PONG.putFloor(scene, X_SIZE_MAP);

	const light = PONG.createLight(scene, X_SIZE_MAP);

	// ------------------------------------keys------------------------------------
	let keys = {};
	document.addEventListener('keydown', (e) => keys[e.key] = true);
	document.addEventListener('keyup', (e) => keys[e.key] = false);


	let display = PONG.createCamera(renderer, X_SIZE_MAP);
	const arena = new Arena(scene);
	const ball = new Ball(scene);

	let sideDefined = new Promise(resolve => {
		let checkInterval = setInterval(() => {
			if (side != "not assigned") {
				clearInterval(checkInterval);
				resolve();
			}
		}, 100);
	});
	sideDefined.then(() => {
		const playerLocal = new Player(side, scene);
		let otherSide = "left";
		if (side == otherSide)
			otherSide = "right";
		const playerSocket = new Player(otherSide, scene);
		PONG.updateScore(scene, playerLocal, playerSocket, game);
		game.going = true;

		let lastTime = 0;
		// ------------------------------------loop------------------------------------
		function animate(currentTime) {
			if (lastTime) {
				let delta = (currentTime - lastTime) / 10;
				if (PONG.isGameGoing(game)) {
					playerLocal.move(keys, arena, delta);
					playerSocket.cube.position.z = enemyPosition;
				}
				if (PONG.isGameStarting(game)) {
					game.memGoing = true;
					ball.reset(scene, playerLocal, playerSocket, game);
				}
				// ball.move(scene, playerLocal, playerSocket, arena, game, delta);
				PONG.lightFollowTarget(light.spot, ball.cube);
				display.controls.update();
				renderer.render(scene, display.camera);
				sendPlayerPosition(playerLocal);
			}
			lastTime = currentTime;
			requestAnimationFrame(animate);
		}

		animate();
	});
}
