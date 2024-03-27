import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

import { doRequest} from '../../utils/fetch.js'

import * as UTILS from '../threeJsUtils.js';
import * as PONG from './pongUtils.js';
import * as JS_UTILS from '../jsUtils.js';
import * as SOCKET from './socketUtils.js';

import { Arena } from './class/Arena.js';
import { Player } from './class/Player.js';
import { Ball } from './class/Ball.js';

export const X_SIZE_MAP = 20;

function windowListener(game) {
    window.addEventListener('hashchange', function () {
        game.going = false;
        if (game.socket.readyState == 1)
        {
            SOCKET.sendLeaveGame(game);
            game.socket.close();
        }
    });

    window.addEventListener('beforeunload', function () {
        game.going = false;
        if (game.socket.readyState == 1)
        {
            SOCKET.sendLeaveGame(game);
            game.socket.close();
        }
    });

    window.addEventListener('resize', function () {
        UTILS.resizeRenderer(game.renderer, game.display.camera);
    });

    document.addEventListener('keydown', (e) => (game.keys[e.key] = true));
    document.addEventListener('keyup', (e) => (game.keys[e.key] = false));
}

function sideDefinedPromise(game) {
    return new Promise((resolve) => {
        let checkInterval = setInterval(() => {
            if (game.side != null) {
                clearInterval(checkInterval);
                resolve();
            }
        }, 100);
    });
}

function doMoveAndCom(game, keys, delta) {
    if (game.needStop == false) {
        game.playerLocal.move(keys, game.arena, delta);
        game.playerSocket.cube.position.z = game.enemyPosition;
        game.ball.cube.position.x = game.ballPosition.x;
        game.ball.cube.position.z = game.ballPosition.z;
        SOCKET.sendPlayerPosition(game.playerLocal, game);
    } else {
        game.playerLocal.reset();
        game.playerSocket.reset();
        game.ball.cube.position.x = 0;
        game.ball.cube.position.z = 0;
        game.going = false;
    }
}

export async function pong3D() {
    const hashQuery = new URLSearchParams(window.location.hash.split('?')[1]);
    const socketPath = hashQuery.get('url');
    if (!socketPath) {
        // console.error('No socket path');
        window.location.hash = 'home';
        return;
    }

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
        light: null,
        keys: {},
    };
    game.display = PONG.createCamera(game.renderer, X_SIZE_MAP)
    game.light = PONG.createLight(game.scene, X_SIZE_MAP);
    JS_UTILS.eraseCookie('username');

    UTILS.createContainerForGame('pong', game.renderer);
    PONG.putTitle(game.scene);
    PONG.putFloor(game.scene, X_SIZE_MAP);

    game.arena = new Arena(game.scene);
    game.ball = new Ball(game.scene);

    windowListener(game);
    SOCKET.socketListener(game);

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
            doMoveAndCom(game, game.keys, delta);
            PONG.lightFollowTarget(game.light.spot, game.ball.cube);
            game.renderer.render(game.scene, game.display.camera);
        }
        lastTime = currentTime;
        requestAnimationFrame(animate);
    }

    animate();
}
