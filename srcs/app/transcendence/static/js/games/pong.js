import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

import * as UTILS from './threeJsUtils.js';
import * as PONG from './pongUtils.js';

import * as JS_UTILS from './jsUtils.js';

const X_SIZE_MAP = 20;

// ------------------------------------classes------------------------------------
class Arena {
    constructor(scene) {
        this.cube = new THREE.LineSegments(
            new THREE.EdgesGeometry(new THREE.BoxGeometry(X_SIZE_MAP, 1, 20)),
            new THREE.LineBasicMaterial({ color: 0xffffff, linewidth: 2 })
        );
        this.hitbox = new THREE.Box3().setFromObject(this.cube);

        scene.add(this.cube);
    }
}

class Player {
    constructor(playerType, scene, game) {
        this.type = playerType;
        this.speed = 0.1;
        this.size = 2;
        this.score = 0;
        this.keys = {
            up: '',
            down: '',
        };
        let color = { color: 0xff0000 };
        if (playerType == game.side) {
            color = { color: 0x0000ff };
            this.keys = {
                up: 'ArrowUp',
                down: 'ArrowDown',
            };
        }
        this.cube = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.5, this.size), new THREE.MeshStandardMaterial(color));
        this.hitbox = new THREE.Box3().setFromObject(this.cube);

        if (playerType == 'left') {
            this.cube.position.x = -(X_SIZE_MAP / 2) + 1;
        } else if (playerType == 'right') {
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
        this.direction = new THREE.Vector3(0, 0, 0);
        this.cube = new THREE.Mesh(
            new THREE.SphereGeometry(0.4, 32, 32),
            new THREE.MeshStandardMaterial({ color: 0x00ff00 })
        );
        this.hitbox = new THREE.Box3().setFromObject(this.cube);

        this.cube.position.y = -0.2;

        UTILS.addShadowsToMesh(this.cube);
        scene.add(this.cube);
    }
}

function sendPlayerPosition(player, game) {
    let message = {
        game: 'player position',
        id: game.secretId,
        username: game.username,
        position: player.cube.position.z,
    };
    JS_UTILS.sendMessageToSocket(game.socket, message);
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

function parseMessage(message, game, scene) {
    if ('game' in message) {
        if (message['game'] == 'starting') {
            game.side = message['side'];
        }
        if (message['game'] == 'positions') {
            if (game.side == 'left') game.enemyPosition = message['playerRight'];
            else if (game.side == 'right') game.enemyPosition = message['playerLeft'];
            game.ballPosition.x = message['positionBallX'];
            game.ballPosition.z = message['positionBallZ'];
        }
        if (message['game'] == 'score') {
            PONG.updateScore(scene, message['score'], game);
            game.playerLocal.reset();
        }
        if (message['game'] == 'end') {
            game.needStop = true;
        }
    }
}

function socketListener(game, scene) {
    game.socket.onopen = function () {
        console.log('Connection established');
        sendStartingGame(game);
    };

    game.socket.onmessage = function (e) {
        let data = JSON.parse(e.data);
        // console.log('Received message: ' + e.data);
        parseMessage(data, game, scene);
    };

    game.socket.onclose = function () {
        console.log('Connection closed');
    };

    game.socket.onerror = function (error) {
        console.log(`socket error: ${error}`);
        console.error(error);
    };

    window.addEventListener('hashchange', function () {
        game.going = false;
        if (game.socket.readyState == 1)
        {
            sendLeaveGame(game);
            game.socket.close();
        }
    });
}

function sideDefinedPromise(game) {
    return new Promise((resolve) => {
        let checkInterval = setInterval(() => {
            console.log('waiting for side');
            if (game.side != null) {
                clearInterval(checkInterval);
                resolve();
            }
        }, 100);
    });
}

function communication(game, keys, delta) {
    if (game.needStop == false) {
        game.playerLocal.move(keys, game.arena, delta);
        game.playerSocket.cube.position.z = game.enemyPosition;
        game.ball.cube.position.x = game.ballPosition.x;
        game.ball.cube.position.z = game.ballPosition.z;
        sendPlayerPosition(game.playerLocal, game);
    } else {
        game.going = false;
        game.playerLocal.reset();
        game.playerSocket.reset();
        game.ball.cube.position.x = 0;
        game.ball.cube.position.z = 0;
    }
}

export async function pong3D() {
    // Get the socket url
    const socketPath = JS_UTILS.readCookie('url');
    JS_UTILS.eraseCookie('url');
    const url = `wss://${window.location.host}/${socketPath}`;
    let splittedURL = url.split('/');

    let game = {
        going: true,
        needStop: false,
        username: JS_UTILS.readCookie('username'),
        side: null,
        textScore: null,
        enemyPosition: 0,
        ballPosition: { x: 0, y: -0.2, z: 0 },
        socket: new WebSocket(url),
        secretId: splittedURL[splittedURL.length - 1],
        playerLocal: null,
        playerSocket: null,
        ball: null,
        arena: null,
    };
    JS_UTILS.eraseCookie('username');

    const scene = UTILS.createScene();
    socketListener(game, scene);
    const renderer = UTILS.createRenderer();
    UTILS.createContainerForGame('pong', renderer);
    PONG.putTitle(scene);
    PONG.putFloor(scene, X_SIZE_MAP);

    const light = PONG.createLight(scene, X_SIZE_MAP);

    // ------------------------------------keys------------------------------------
    let keys = {};
    document.addEventListener('keydown', (e) => (keys[e.key] = true));
    document.addEventListener('keyup', (e) => (keys[e.key] = false));

    let display = PONG.createCamera(renderer, X_SIZE_MAP);
    game.arena = new Arena(scene);
    game.ball = new Ball(scene);

    await sideDefinedPromise(game);

    game.playerLocal = new Player(game.side, scene, game);
    let otherSide = 'left';
    if (game.side == otherSide) otherSide = 'right';
    game.playerSocket = new Player(otherSide, scene, game);
    PONG.updateScore(scene, '0 - 0', game);

    let lastTime = 0;
    // ------------------------------------loop------------------------------------
    function animate(currentTime) {
        if (lastTime && game.going == true) {
            let delta = (currentTime - lastTime) / 10;
            display.controls.update();
            communication(game, keys, delta);
            PONG.lightFollowTarget(light.spot, game.ball.cube);
            renderer.render(scene, display.camera);
        }
        lastTime = currentTime;
        requestAnimationFrame(animate);
    }

    animate();
}
