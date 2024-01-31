import { FontLoader } from 'three/addons/loaders/FontLoader.js';
import { TextGeometry } from 'three/addons/geometries/TextGeometry.js';

// Font gestion
let theFont;
function loadFont(url) {
	return new Promise((resolve, reject) => {
		const loader = new FontLoader();

		loader.load(url, function (font) {
			resolve(font);
		}, undefined, function (error) {
			reject(error);
		});
	});
}

// Wait for the font to be loaded (async)
await loadFont('https://threejs.org/examples/fonts/helvetiker_regular.typeface.json')
	.then(font => {
		theFont = font;
	})
	.catch(error => {
		console.log("the font could not be loaded: " + error);
	});

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

export function createScene(text) {
	const scene = new THREE.Scene();
	if (text)
		scene.background = text;
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

export function resizeRenderer(renderer, fullScreen = false) {
	const headerRect = document.querySelector('header').getBoundingClientRect();
	const footerRect = document.querySelector('footer').getBoundingClientRect();
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

	const button = document.createElement("button");
	gameName = gameName.charAt(0).toUpperCase() + gameName.slice(1);
	button.id = "button" + gameName;
	button.innerHTML = "PLAY";
	container.appendChild(button);
	container.appendChild(gameRenderer.domElement);
	return button;
}