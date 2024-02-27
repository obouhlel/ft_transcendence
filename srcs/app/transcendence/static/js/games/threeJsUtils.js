import { FontLoader } from 'three/addons/loaders/FontLoader.js';
import { TextGeometry } from 'three/addons/geometries/TextGeometry.js';

// Font gestion
export let theFont;

async function loadAndSetFont(url) {
    try {
        const font = await new Promise((resolve, reject) => {
            const loader = new FontLoader();

            loader.load(url, function (font) {
                resolve(font);
            }, undefined, function (error) {
                reject(error);
            });
        });

        theFont = font;
    }
	catch (error) {
        console.log("the font could not be loaded: " + error);
    }
}

// loadAndSetFont('https://threejs.org/examples/fonts/helvetiker_regular.typeface.json');
loadAndSetFont('./font/helvetiker_regular.typeface.json');

export function doTextGeo(text, fontSize, threeD = false) {
	return new TextGeometry( text, {
		font: theFont,
		size: fontSize,
		height: 1 * threeD,
		curveSegments: 12,
		bevelEnabled: threeD,
		bevelThickness: 0.01,
		bevelSize: 0.1,
		bevelOffset: 0,
		bevelSegments: 5
	} );
}

export function createScene(color = 0x000000) {
	const scene = new THREE.Scene();
	scene.background = new THREE.Color(color);
	return scene;
}

export function createRenderer() {
	const headerRect = document.querySelector('header').getBoundingClientRect();
	const footerRect = document.querySelector('footer').getBoundingClientRect();
	const renderer = new THREE.WebGLRenderer();
	renderer.setSize(window.innerWidth, window.innerHeight - headerRect.bottom - footerRect.bottom);
	renderer.shadowMap.enabled = true;
	renderer.shadowMap.type = THREE.PCFSoftShadowMap;
	return renderer;
}

export function resizeRenderer(renderer, camera, fullScreen = false) {
	const headerRect = document.querySelector('header');
	const footerRect = document.querySelector('footer');

	camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
	if (fullScreen) {
		headerRect.style.display = "none";
		footerRect.style.display = "none";
	} else {
		headerRect.style.display = "block";
		footerRect.style.display = "block";
	}
	renderer.setSize(window.innerWidth, window.innerHeight - headerRect.bottom - footerRect.bottom);
}

export function createContainerForGame(gameName, gameRenderer) {
	const main = document.querySelector("main");

	const container = document.createElement("div");
	container.id = gameName;
	main.appendChild(container);

	container.appendChild(gameRenderer.domElement);
}

export function addShadowsToMesh(mesh) {
	mesh.castShadow = true;
	mesh.receiveShadow = true;
}