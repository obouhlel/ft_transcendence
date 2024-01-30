import * as THREE from 'three';
import { PointerLockControls } from 'three/addons/controls/PointerLockControls.js';

import { doTextGeo } from './textFont.js';

// 1 => wall
// 0 => space
// 3, 4 => spaws
const map = [
	[1, 1, 1, 1, 1, 1, 1, 1],
	[1, 3, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 1, 0, 0, 1],
	[1, 0, 0, 1, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 4, 1],
	[1, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 1, 1, 1, 1]
];
const sizeBox = 5;
const widthMap = map[0].length * sizeBox;
const heightMap = map.length *sizeBox;

function blitMap(scene) {
	const floor = new THREE.Mesh( new THREE.BoxGeometry( widthMap, 0.1, heightMap ), new THREE.MeshStandardMaterial( { color: 0xffffff } ) );
	const bloc = new THREE.Mesh( new THREE.BoxGeometry( sizeBox, sizeBox, sizeBox ), new THREE.MeshStandardMaterial( { color: 0xffffff } ) );
	floor.receiveShadow = true;
	floor.castShadow = true;
	bloc.receiveShadow = true;
	bloc.castShadow = true;


	floor.position.x += widthMap / 2;
	floor.position.z += heightMap / 2;
	scene.add(floor);
	for (let z = 0; z < map.length; z++) {
		for (let x = 0; x < map[z].length; x++) {
			if (map[z][x] == 1) {
				let blocCpy = bloc.clone();
				blocCpy.position.set((x * sizeBox) + sizeBox/2, sizeBox/2, (z * sizeBox) + sizeBox/2);
				scene.add(blocCpy);
			}
		}
	}
}

export function shooter() {
	class Player {
		constructor(name, x, z) {
			this.name = name;
			this.speed = 0.2;
			this.pos = new THREE.Vector3(x, 0, z);
			this.dir = new THREE.Vector3(0, 0, 0);
			this.hp = 150;
			this.dmg = 30;
			this.ammo = 8;
		}

		move(keys) {
			let vecMove = new THREE.Vector3();
			if (keys['w']) {
				let front = new THREE.Vector3();
				front = this.dir.normalize().multiplyScalar(this.speed);
				vecMove.add(front);
			}
			if (keys['s']) {
				let back = new THREE.Vector3();
				back = this.dir.normalize().multiplyScalar(-this.speed);
				vecMove.add(back);
			}
			if (keys['a']) {
				let left = new THREE.Vector3();
				left.crossVectors(new THREE.Vector3(0, 1, 0), this.dir).normalize().multiplyScalar(this.speed);
				vecMove.add(left);
			}
			if (keys['d']) {
				let right = new THREE.Vector3();
				right.crossVectors(this.dir, new THREE.Vector3(0, 1, 0)).normalize().multiplyScalar(this.speed);
				vecMove.add(right);
			}
			vecMove.y = 0;
			console.log(vecMove);
			vecMove.normalize().multiplyScalar(this.speed);
			this.pos.add(vecMove);
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

	blitMap(scene);

	// Keys
	let keys = {};
	document.addEventListener('keydown', (e) => keys[e.key] = true);
	document.addEventListener('keyup', (e) => keys[e.key] = false);

	// Light
	const globalLight = new THREE.DirectionalLight(0xffffff, 1);
	globalLight.position.set(widthMap/2, 20, heightMap);
	globalLight.target.position.set(widthMap/2, 0, heightMap/2);
	scene.add(globalLight.target);

	globalLight.castShadow = true;

	globalLight.shadow.camera.left = -(widthMap / 2);
	globalLight.shadow.camera.right = widthMap / 2;
	globalLight.shadow.camera.top = heightMap/2;
	globalLight.shadow.camera.bottom = -heightMap/2;
	globalLight.shadow.camera.near = 0.5;
	globalLight.shadow.camera.far = 500;

	let help = new THREE.DirectionalLightHelper(globalLight);
	scene.add(help);
	const leftLight = globalLight.clone();
	const rightLight = globalLight.clone();
	const topLight = globalLight.clone();
	leftLight.position.set(widthMap, 20, heightMap/2);
	rightLight.position.set(0, 20, heightMap/2);
	topLight.position.set(widthMap/2, 20, 0);
	scene.add(topLight);
	scene.add(leftLight);
	scene.add(rightLight);
 	scene.add(globalLight);

	// Loop
	function animate() {
		requestAnimationFrame(animate);

		player.move(keys);
		camera.position.x = player.pos.x;
		camera.position.y = player.pos.y + 2;
		camera.position.z = player.pos.z;
		camera.getWorldDirection(player.dir);

		renderer.render(scene, camera);
	}

	animate();
}