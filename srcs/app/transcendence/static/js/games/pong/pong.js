import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

import { doRequest} from '../../utils/fetch.js'

import * as UTILS from '../threeJsUtils.js';
import * as PONG from './pongUtils.js';
import * as JS_UTILS from '../jsUtils.js';

import { Arena } from './class/Arena.js';
import { Player } from './class/Player.js';
import { Ball } from './class/Ball.js';

export const X_SIZE_MAP = 20;

// ------------------------------------classes------------------------------------

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

function parseMessage(message, game) {
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
            PONG.updateScore(game.scene, message['score'], game);
            game.playerLocal.reset();
        }
        if (message['game'] == 'end') {
            game.needStop = true;
        }
    }
}

function socketListener(game) {
    game.socket.onopen = function () {
        console.log('Connection established');
        sendStartingGame(game);
    };

    game.socket.onmessage = function (e) {
        let data = JSON.parse(e.data);
        // console.log('Received message: ' + e.data);
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
        game.going = false;
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
    const splittedURL = url.split('/');

    const game = {
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
        scene: UTILS.createScene(),
        renderer: UTILS.createRenderer(),
        display: null,
    };
    game.display = PONG.createCamera(game.renderer, X_SIZE_MAP)
    JS_UTILS.eraseCookie('username');

    UTILS.createContainerForGame('pong', game.renderer);
    PONG.putTitle(game.scene);
    PONG.putFloor(game.scene, X_SIZE_MAP);

    const light = PONG.createLight(game.scene, X_SIZE_MAP);

    // ------------------------------------keys------------------------------------
    let keys = {};
    document.addEventListener('keydown', (e) => (keys[e.key] = true));
    document.addEventListener('keyup', (e) => (keys[e.key] = false));

    game.arena = new Arena(game.scene);
    game.ball = new Ball(game.scene);

    socketListener(game);

    await sideDefinedPromise(game);

    game.playerLocal = new Player(game.side, game.scene, game);
    let otherSide = 'left';
    if (game.side == otherSide) otherSide = 'right';
    game.playerSocket = new Player(otherSide, game.scene, game);
    PONG.updateScore(game.scene, '0 - 0', game);

    let lastTime = 0;
    // ------------------------------------loop------------------------------------
    function animate(currentTime) {
        if (lastTime && game.going == true) {
            const delta = (currentTime - lastTime) / 10;
            game.display.controls.update();
            communication(game, keys, delta);
            PONG.lightFollowTarget(light.spot, game.ball.cube);
            game.renderer.render(game.scene, game.display.camera);
        }
        lastTime = currentTime;
        requestAnimationFrame(animate);
    }

    animate();
}
