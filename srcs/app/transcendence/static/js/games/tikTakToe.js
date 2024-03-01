import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

import * as UTILS from './threeJsUtils.js';
import * as JS_UTILS from './jsUtils.js';
import * as TIK_TAK_TOE from './tikTakToeUtils.js';

const X_SIZE_MAP = 24;
const SIZE_CASE = X_SIZE_MAP / 3;

class PawnCross {
    constructor(scene, x, z) {
        this.geometry = new THREE.BoxGeometry(1, 1, 1);
        this.material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
        this.cube = new THREE.Mesh(this.geometry, this.material);
        this.cube.position.x = x;
        this.cube.position.z = z;
        this.cube.position.y = 5;
        scene.add(this.cube);
    }
}

class PawnCircle {
    constructor(scene, x, z) {
        let geometry = new THREE.SphereGeometry(0.5, 32, 32);
        let material = new THREE.MeshBasicMaterial({ color: 0x0000ff });
        this.cube = new THREE.Mesh(geometry, material);
        this.cube.position.x = x;
        this.cube.position.z = z;
        this.cube.position.y = 5;
        scene.add(this.cube);
    }
}

class Case {
    constructor(scene, x, z, name) {
        this.cube = new THREE.LineSegments(
            new THREE.EdgesGeometry(new THREE.BoxGeometry(SIZE_CASE, 1, SIZE_CASE)),
            new THREE.LineBasicMaterial({ color: 0xffffff, linewidth: 2 })
        );
        this.cube.position.x = x;
        this.cube.position.z = z;

        this.floor = TIK_TAK_TOE.putFloor(scene, SIZE_CASE);
        this.floor.position.x = x;
        this.floor.position.z = z;
        this.floor.userData.name = name;
        this.floor.userData.clickable = true;

        this.pawnOnThis = null;
            
        scene.add(this.cube);
        scene.add(this.floor);
    }

    getPawnDown() {
        if (this.pawnOnThis != null && this.pawnOnThis.cube.position.y > 0) {
            this.pawnOnThis.cube.position.y -= 0.1;
        }
    }
}

function createArena(scene) {
    const arena = [];
    for (let i = 0; i < 3; i++) {
        arena.push([]);
        for (let j = 0; j < 3; j++) {
            const x = i * SIZE_CASE + i;
            const z = j * SIZE_CASE + j;
            const name = { x: i, z: j}
            arena[i].push(new Case(scene, x, z, name));
        }
    }
    return arena;
}

function getPawn(game) {
    if (game.pawnStr == 'O') {
        return new PawnCircle(game.scene, 0, 0);
    } else if (game.pawnStr == 'X') {
        return new PawnCross(game.scene, 0, 0);
    }
    return null;
}

function parseMessage(data, game) {
    if ('game' in data) {
        if (data['game'] == 'starting') {
            game.pawnStr = data['pawn'];
            game.pawn = getPawn(game);
        }
        if (data['game'] == 'play') {
            game.isMyTurn = true;
        }
        if (data['game'] == 'position') {
            let pawn = null;
            if (game.pawnStr == 'O') {
                pawn = new PawnCross(game.scene, 0, 0);
            } else if (game.pawnStr == 'X') {
                pawn = new PawnCircle(game.scene, 0, 0);
            }
            pawn.cube.position.x = game.arena[data['x']][data['z']].floor.position.x;
            pawn.cube.position.z = game.arena[data['x']][data['z']].floor.position.z;
            game.arena[data['x']][data['z']].pawnOnThis = pawn;
        }
        if (data['game'] == 'end') {
            
        }
    }
}

function sendStartingGame(game) {
    let message = {
        game: 'starting',
        id: game.secretId,
        username: game.username,
    };
    JS_UTILS.sendMessageToSocket(game.socket, message);
}

function sendLeaveGame(game) {
    let message = {
        game: 'leaved',
        id: game.secretId,
        username: game.username,
    };
    JS_UTILS.sendMessageToSocket(game.socket, message);
}

function sendNewPawnPosition(game, x, z) {
    let message = {
        game: 'position',
        id: game.secretId,
        username: game.username,
        x: x,
        y: z,
    };
    JS_UTILS.sendMessageToSocket(game.socket, message);
}

function socketListener(game) {
    game.socket.onopen = function () {
        console.log('Connection established');
        sendStartingGame(game);
    };

    game.socket.onmessage = function (e) {
        let data = JSON.parse(e.data);
        console.log('Received message: ' + e.data);
        parseMessage(data, game);
    };

    game.socket.onclose = function () {
        console.log('Connection closed');
    };

    game.socket.onerror = function (error) {
        console.log(`socket error: ${error}`);
        console.error(error);
    };

    window.addEventListener('hashchange', function () {
        if (game.socket.readyState == 1)
        {
            sendLeaveGame(game);
            game.socket.close();
        }
    });

    window.addEventListener('resize', function () {
        console.log('window size: ' + window.innerWidth + 'x' + window.innerHeight);
        UTILS.resizeRenderer(game.renderer, game.display.camera);
    });
}

function move(keys, game) {
    if (keys['ArrowUp'] == 'down' && game.previewPosition.z > 0) {
        game.previewPosition.z -= 1;
        keys['ArrowUp'] = 'done';
    }
    if (keys['ArrowDown'] == 'down' && game.previewPosition.z < game.arena.length - 1) {
        game.previewPosition.z += 1;
        keys['ArrowDown'] = 'done';
    }
    if (keys['ArrowLeft'] == 'down' && game.previewPosition.x > 0) {
        game.previewPosition.x -= 1;
        keys['ArrowLeft'] = 'done';
    }
    if (keys['ArrowRight'] == 'down' && game.previewPosition.x < game.arena.length - 1) {
        game.previewPosition.x += 1;
        keys['ArrowRight'] = 'done';
    }
}

function printPrev(keys, game) {
    const arenaCase = game.arena[game.previewPosition.x][game.previewPosition.z];
    game.pawn.cube.position.x = arenaCase.floor.position.x;
    game.pawn.cube.position.z = arenaCase.floor.position.z;
    if (arenaCase.pawnOnThis == null && game.isMyTurn) {
        game.pawn.cube.material.color.set('green');
        if (keys[' '] == 'down') {
            keys[' '] = 'done';
            game.isMyTurn = false;
            arenaCase.pawnOnThis = game.pawn;
            game.pawn = getPawn(game);
            sendNewPawnPosition(game, game.previewPosition.x, game.previewPosition.z); 
        }
    }
    else {
        game.pawn.cube.material.color.set('red');
    }
}

function waitPawnSelection(game) {
    return new Promise((resolve) => {
        let checkInterval = setInterval(() => {
            if (game.pawnStr != null) {
                clearInterval(checkInterval);
                resolve();
            }
        }, 100);
    });
}

export async function tikTakToe3D() {
	const socketPath = JS_UTILS.readCookie('url');
    JS_UTILS.eraseCookie('url');
    const url = `wss://${window.location.host}/${socketPath}`;
    const splittedURL = url.split('/');

    const game = {
        secretId: splittedURL[splittedURL.length - 1],
        socket: null,
        username: JS_UTILS.readCookie('username'),
        pawnStr: null,
        pawn: null,
        previewPosition: { x: 1, z: 1 },
        isMyTurn: false,
        arena: null,
        scene: UTILS.createScene(),
        renderer: UTILS.createRenderer(),
        display: null,
    };
    game.socket = new WebSocket(url);
    UTILS.createContainerForGame('tikTakToe', game.renderer);
    JS_UTILS.eraseCookie('username');
    game.arena = createArena(game.scene);
    game.display = TIK_TAK_TOE.createCamera(game.renderer, X_SIZE_MAP);

    socketListener(game);
    await waitPawnSelection(game);

    // ------------------------------------keys------------------------------------
    const keys = {};
    document.addEventListener('keydown', function(e) {
        if (keys[e.key] == 'up')
            keys[e.key] = 'down';
    });
    document.addEventListener('keyup', function(e) { 
        keys[e.key] = 'up';
    });

    let lastTime = 0;
    // ------------------------------------loop------------------------------------
    function animate(currentTime) {
        if (lastTime) {
            const delta = (currentTime - lastTime) / 10;
            move(keys, game);
            printPrev(keys,game);
            for (let i = 0; i < game.arena.length; i++) {
                for (let j = 0; j < game.arena[i].length; j++) {
                    game.arena[i][j].getPawnDown();
                }
            }
            game.renderer.render(game.scene, game.display.camera);
        }
        lastTime = currentTime;
        requestAnimationFrame(animate);
    }

    animate();
}