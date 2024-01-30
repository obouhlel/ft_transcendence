import { theFont } from "./pong.js";
import * as THREE from 'three';

export function shooter() {
	class Player {
		constructor(name, x, y) {
			this.name = name;
			this.pos = THREE.Vector2(x, y);
			this.hp = 150;
			this.dmg = 30;
			this.ammo = 8;
		}

		move() {

		}

		shoot() {

		}

		takeDmg() {

		}
	}

	let going = false;
	let memGoing = false;

	const main = document.querySelector("main");

	const container = document.createElement("div");
	container.id = "pong";
	main.appendChild(container);

	const button = document.createElement("button");
	button.id = "buttonPong3D";
	button.innerHTML = "PLAY";
	container.appendChild(button);
	button.addEventListener("click", () => {
		going = true;
		button.style.display = "none";
		playerLeft.score = 0;
		playerRight.score = 0;
	});

	// Get the header and footer rect box
	const headerRect = document.querySelector('header').getBoundingClientRect();
	const footerRect = document.querySelector('footer').getBoundingClientRect();

	const scene = new THREE.Scene();
	const renderer = new THREE.WebGLRenderer();
	renderer.setSize(window.innerWidth, window.innerHeight - headerRect.bottom - footerRect.bottom);
	renderer.shadowMap.enabled = true;
	renderer.shadowMap.type = THREE.PCFSoftShadowMap;
	container.appendChild(renderer.domElement);

	// Camera
	const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
	camera.position.y = -10;
	camera.position.z = 20 - 5;
	camera.rotation.x = 0.55;

	function animate() {
		requestAnimationFrame(animate);



		renderer.render(scene, camera);
	}

	animate();
}