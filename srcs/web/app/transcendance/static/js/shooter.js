import * as THREE from 'three';
import { PointerLockControls } from 'three/addons/controls/PointerLockControls.js';

import { doTextGeo } from './textFont.js';

const map = [1, 1, 1, 1, 1, 1, 1, 1,
			 1, 0, 0, 0, 0, 0, 0, 1,
			 1, 0, 0, 0, 0, 0, 0, 1,
			 1, 0, 0, 0, 1, 0, 0, 1,
			 1, 0, 0, 1, 0, 0, 0, 1,
			 1, 0, 0, 0, 0, 0, 0, 1,
			 1, 0, 0, 0, 0, 0, 0, 1,
			 1, 0, 0, 0, 0, 0, 0, 1,
			 1, 1, 1, 1, 1, 1, 1, 1,];

export function shooter() {
	class Player {
		constructor(name, x, z) {
			this.name = name;
			this.speed = 0.1;
			this.pos = new THREE.Vector3(x, 0, z);
			this.dir = new THREE.Vector3(0, 0, 0);
			this.hp = 150;
			this.dmg = 30;
			this.ammo = 8;
		}

		move(keys) {
			if (keys['w']) {
				this.speed = 0.1;
				if (keys['shift']) {
					this.speed = 0.2;
				}
			}
			if (keys['s']) {
				this.speed = -0.1;
			}
		}

		shoot(keys) {

		}

		takeDmg() {

		}
	}

	let going = false;
	let memGoing = false;

	// HTML Generator
	const main = document.querySelector("main");

	const container = document.createElement("div");
	container.id = "shooter";
	main.appendChild(container);

	const button = document.createElement("button");
	button.id = "buttonShooter3D";
	button.innerHTML = "PLAY";
	container.appendChild(button);
	button.addEventListener("click", () => {
		going = true;
		button.style.display = "none";
	});

	// Create game window
	const headerRect = document.querySelector('header').getBoundingClientRect();
	const footerRect = document.querySelector('footer').getBoundingClientRect();

	const scene = new THREE.Scene();
	const renderer = new THREE.WebGLRenderer();
	renderer.setSize(window.innerWidth, window.innerHeight - headerRect.bottom - footerRect.bottom);
	renderer.shadowMap.enabled = true;
	renderer.shadowMap.type = THREE.PCFSoftShadowMap;
	container.appendChild(renderer.domElement);

	// Player
	let player = new Player("test", 0, 0);

	// Camera
	const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
	camera.position.x = player.pos.x;
	camera.position.y = player.pos.y + 2;
	camera.position.z = player.pos.z;

	// Mouse
	let controls = new PointerLockControls(camera, renderer.domElement);

	document.addEventListener('click', function () {
		controls.lock();
	});

	// Cursor


	// Floor
	const floor = new THREE.Mesh(new THREE.BoxGeometry(20, 0.1, 20), new THREE.MeshStandardMaterial({ color: 0xffffff }));
	floor.receiveShadow = true;
	floor.castShadow = true;
	scene.add(floor);

	// Keys
	let keys = {};
	document.addEventListener('keydown', (e) => keys[e.key] = true);
	document.addEventListener('keyup', (e) => keys[e.key] = false);

	// Light
	const globalLight = new THREE.DirectionalLight(0xffffff, 1);
	globalLight.position.set(0, 20, 0);

	globalLight.castShadow = true;

	globalLight.shadow.camera.left = -(20 / 2);
	globalLight.shadow.camera.right = 20 / 2;
	globalLight.shadow.camera.top = 10;
	globalLight.shadow.camera.bottom = -10;
	globalLight.shadow.camera.near = 0.5;
	globalLight.shadow.camera.far = 500;

	scene.add(globalLight);

	// Loop
	function animate() {
		requestAnimationFrame(animate);

		player.move(keys);
		camera.position.x = player.pos.x;
		camera.position.y = player.pos.y + 2;
		camera.position.z = player.pos.z;
		camera.getWorldDirection(player.dir);

		player.dir.y = 0;
		player.dir.normalize();
		player.dir.multiplyScalar(player.speed);
		player.pos.add(player.dir);
		player.speed = 0;
		renderer.render(scene, camera);
	}

	animate();
}