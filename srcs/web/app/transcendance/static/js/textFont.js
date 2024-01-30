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