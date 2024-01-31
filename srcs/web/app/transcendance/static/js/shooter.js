import * as THREE from 'three';
import { PointerLockControls } from 'three/addons/controls/PointerLockControls.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

import * as UTILS from './threeJsUtils.js';

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
const heightMap = map.length * sizeBox;

let wall;
let ground;
let roof;
export function loadTexture(url) {
	return new Promise((resolve, reject) => {
		const loader = new THREE.TextureLoader();

		loader.load(url, function (texture) {
			resolve(texture);
		}, undefined, function (error) {
			reject(error);
		});
	});
}

await loadTexture('/static/img/ground.jpg')
	.then(texture => {
		ground = texture;
	})
	.catch(error => {
		console.log("the texture could not be loaded: " + error);
	});

await loadTexture('/static/img/brickWall.jpg')
	.then(texture => {
		wall = texture;
	})
	.catch(error => {
		console.log("the texture could not be loaded: " + error);
	});

await loadTexture('/static/img/ceil.jpg')
	.then(texture => {
		roof = texture;
	})
	.catch(error => {
		console.log("the texture could not be loaded: " + error);
	});

function blitMap(scene) {
	ground.repeat.set(1, 1);
	const ceil = new THREE.Mesh(new THREE.BoxGeometry(widthMap, 0.1, heightMap), new THREE.MeshBasicMaterial({ map: roof }));
	const floor = new THREE.Mesh(new THREE.BoxGeometry(widthMap, 0.1, heightMap), new THREE.MeshBasicMaterial({ map: ground }));
	const bloc = new THREE.Mesh(new THREE.BoxGeometry(sizeBox, sizeBox, sizeBox), new THREE.MeshBasicMaterial({ map: wall }));
	floor.receiveShadow = true;
	floor.castShadow = true;
	bloc.receiveShadow = true;
	bloc.castShadow = true;


	ceil.position.y += sizeBox;
	ceil.position.x += widthMap / 2;
	ceil.position.z += heightMap / 2;
	floor.position.x += widthMap / 2;
	floor.position.z += heightMap / 2;
	scene.add(ceil);
	scene.add(floor);
	for (let z = 0; z < map.length; z++) {
		for (let x = 0; x < map[z].length; x++) {
			if (map[z][x] == 1) {
				let blocCpy = bloc.clone();
				blocCpy.position.set((x * sizeBox) + sizeBox / 2, sizeBox / 2, (z * sizeBox) + sizeBox / 2);
				scene.add(blocCpy);
			}
		}
	}
}

class Player {
	constructor(name, x, z, scene) {
		this.name = name;
		this.speed = 0.2;
		this.body = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.7, 2), new THREE.MeshBasicMaterial({ color: 0x00ff00 }));
		this.weapon = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.1, 1), new THREE.MeshBasicMaterial({ color: 0x0000ff }));
		this.view = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
		this.pos = new THREE.Vector3(x, 0, z);
		this.dir = new THREE.Vector3(0, 0, 0);
		this.hp = 150;
		this.dmg = 30;
		this.ammo = 8;
		this.view.position.set(0, 1, 0);
		this.weapon.position.set(0, -0.7, -0.7); // for the opponent put 0 on y
		this.view.add(this.weapon);
		this.body.add(this.view);
		scene.add(this.body);
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
		vecMove.normalize().multiplyScalar(this.speed);
		this.pos.add(vecMove);
		this.body.position.set(this.pos.x, this.pos.y + 1, this.pos.z + 1);
	}

	shoot(keys) {

	}

	takeDmg() {

	}
}

export function shooter() {

	let going = false;
	let memGoing = false;

	const scene = UTILS.createScene(0xFF0000);
	const renderer = UTILS.createRenderer();
	const button = UTILS.createContainerForGame("shooter", renderer);

	button.addEventListener("click", () => {
		going = true;
		button.style.display = "none";
	});

	// Player
	let player = new Player("test", 10, 10, scene);

	// Camera
	const cameraGlobal = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
	cameraGlobal.position.set(player.pos.x, player.pos.y + 2, player.pos.z);

	document.addEventListener('click', function () {
		controls.lock();
	});

	blitMap(scene);

	// Keys
	let keys = {};
	document.addEventListener('keydown', (e) => keys[e.key] = true);
	document.addEventListener('keyup', (e) => keys[e.key] = false);

	// Light
	const light = new THREE.PointLight(0xffffff, 5, 500);
	light.castShadow = true;
	light.position.set(10, 2, 10);

	scene.add(light);

	// Player controls
	let controls = new PointerLockControls(player.view, renderer.domElement);
	// GAme controls
	let controlsGLobal = new OrbitControls(cameraGlobal, renderer.domElement);
	controlsGLobal.enableRotate = true;
	controlsGLobal.rotateSpeed = 1.0;
	// Loop
	function animate() {
		requestAnimationFrame(animate);

		controlsGLobal.target.set(widthMap / 2, 0, heightMap / 2);
		controlsGLobal.update();
		player.move(keys);
		player.view.getWorldDirection(player.dir);
		// player.body.rotation.copy(player.view.rotation);
		renderer.render(scene, cameraGlobal);
		// renderer.render(scene, player.view);
	}

	animate();
}