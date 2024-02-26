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
	const floor = new THREE.Mesh(new THREE.BoxGeometry(sizeBox, 0.1, sizeBox), new THREE.MeshBasicMaterial({ color: 0x000000}));
	const floorb = new THREE.Mesh(new THREE.BoxGeometry(sizeBox, 0.1, sizeBox), new THREE.MeshBasicMaterial({ color: 0xffffff}));
	const bloc = new THREE.Mesh(new THREE.BoxGeometry(sizeBox, sizeBox, sizeBox), new THREE.MeshBasicMaterial({ map: wall }));
	floor.receiveShadow = true;
	floor.castShadow = true;
	bloc.receiveShadow = true;
	bloc.castShadow = true;


	ceil.position.y = sizeBox;
	ceil.position.x = widthMap / 2;
	ceil.position.z = heightMap / 2;
	// scene.add(ceil);
	for (let z = 0; z < map.length; z++) {
		for (let x = 0; x < map[z].length; x++) {
			if (map[z][x] == 1) {
				let blocCpy = bloc.clone();
				blocCpy.position.set((x * sizeBox) + sizeBox / 2, sizeBox / 2, (z * sizeBox) + sizeBox / 2);
				scene.add(blocCpy);
			}
			let floorCpy;
			// faire un damier
			if (z % 2 == 0) {
				if (x % 2 == 0) {
					floorCpy = floor.clone();
				} else {
					floorCpy = floorb.clone();
				}
			}
			else {
				if (x % 2 == 0) {
					floorCpy = floorb.clone();
				} else {
					floorCpy = floor.clone();
				}
			}
			floorCpy.position.set((x * sizeBox) + sizeBox / 2, 0, (z * sizeBox) + sizeBox / 2);
			scene.add(floorCpy);
		}
	}
}

class Bullet {
	constructor(x, y, z, dir, scene) {
		this.speed = 1;
		this.body = new THREE.Mesh(new THREE.SphereGeometry(0.1), new THREE.MeshBasicMaterial({ color: 0xff0000 }));
		this.pos = new THREE.Vector3(x, y, z);
		this.dir = dir;
		this.body.position.set(this.pos.x, this.pos.y, this.pos.z);
		scene.add(this.body);
	}

	move() {
		let vecMove = new THREE.Vector3();
		vecMove.add(this.dir.normalize().multiplyScalar(this.speed));
		this.pos.add(vecMove);
		this.body.position.set(this.pos.x, this.pos.y, this.pos.z);
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

	move(keys, deltaTime) {
		let vecMove = new THREE.Vector3();
		if (keys['w']) {
			let front = new THREE.Vector3();
			front = this.dir.normalize().multiplyScalar(this.speed * deltaTime);
			vecMove.add(front);
		}
		if (keys['s']) {
			let back = new THREE.Vector3();
			back = this.dir.normalize().multiplyScalar(-this.speed * deltaTime);
			vecMove.add(back);
		}
		if (keys['a']) {
			let left = new THREE.Vector3();
			left.crossVectors(new THREE.Vector3(0, 1, 0), this.dir).normalize().multiplyScalar(this.speed * deltaTime);
			vecMove.add(left);
		}
		if (keys['d']) {
			let right = new THREE.Vector3();
			right.crossVectors(this.dir, new THREE.Vector3(0, 1, 0)).normalize().multiplyScalar(this.speed * deltaTime);
			vecMove.add(right);
		}
		vecMove.y = 0;
		vecMove.normalize().multiplyScalar(this.speed * deltaTime);
		let hitBox = new THREE.Box3().setFromObject(this.body);
		if (this.dir.z > 0) {
			if (map[Math.floor((hitBox.max.z + vecMove.z) / sizeBox)][Math.floor(this.pos.x / sizeBox)] == 1) {
				vecMove.z = 0;
			}
		}
		else if (this.dir.z < 0) {
			if (map[Math.floor((hitBox.min.z + vecMove.z) / sizeBox)][Math.floor(this.pos.x / sizeBox)] == 1) {
				vecMove.z = 0;
			}
		}
		if (this.dir.x > 0) {
			if (map[Math.floor(this.pos.z / sizeBox)][Math.floor((hitBox.max.x + vecMove.x) / sizeBox)] == 1) {
				vecMove.x = 0;
			}
		}
		else if (this.dir.x < 0) {
			if (map[Math.floor(this.pos.z / sizeBox)][Math.floor((hitBox.min.x + vecMove.x) / sizeBox)] == 1) {
				vecMove.x = 0;
			}
		}
		console.log(vecMove);
		this.pos.add(vecMove);
		this.body.position.set(this.pos.x, this.pos.y + 1, this.pos.z + 1);
	}

	shoot() {
		if (this.ammo > 0) {
			console.log("shooter");
			this.ammo--;
		}
	}

	takeDmg() {

	}
}

export function shooter() {

	let going = false;
	let memGoing = false;

	const scene = UTILS.createScene(0xFF0000);
	const renderer = UTILS.createRenderer();

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
	document.addEventListener('keydown', (e) => {
		if (keys[e.key] != 2) {
			keys[e.key] = true;
		}
	});
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

	let lastTime = 0;
	// Loop
	function animate(currentTime) {
		if (lastTime) {
			let delta = (currentTime - lastTime) / 20;
			controlsGLobal.target.set(widthMap / 2, 0, heightMap / 2);
			controlsGLobal.update();
			player.move(keys, delta);
			player.view.getWorldDirection(player.dir);
			// player.body.rotation.copy(player.view.rotation);
			if (keys['b'] == true) {
				player.shoot();
				keys['b'] = 2;
			}
			if (!keys[' ']) {
				renderer.render(scene, cameraGlobal);
			} else {
				renderer.render(scene, player.view);
			}
		}
		lastTime = currentTime;
		requestAnimationFrame(animate);
	}

	animate();
}