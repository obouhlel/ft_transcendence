import * as THREE from "three";

import * as UTILS from "../threeJsUtils.js";
import * as JS_UTILS from "../jsUtils.js";
import * as TIK_TAK_TOE from "./ticTacToeUtils.js";
import * as SOCKET from "./socketUtils.js";

export const X_SIZE_MAP = 24;
export const SIZE_CASE = X_SIZE_MAP / 3;

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

function windowListener(game) {
  window.addEventListener("hashchange", function () {
    if (game.socket.readyState == 1) {
      SOCKET.sendLeaveGame(game);
      game.socket.close();
    }
  });

  window.addEventListener("beforeunload", function () {
    if (game.socket.readyState == 1) {
      SOCKET.sendLeaveGame(game);
      game.socket.close();
    }
  });

  window.addEventListener("resize", function () {
    UTILS.resizeRenderer(game.renderer, game.display.camera);
  });

  document.addEventListener("keydown", function (e) {
    if (game.keys[e.key] == "up") game.keys[e.key] = "down";
  });
  document.addEventListener("keyup", function (e) {
    game.keys[e.key] = "up";
  });
}

export async function ticTacToe3D() {
  const socketPath = JS_UTILS.readCookie("url");
  JS_UTILS.eraseCookie("url");
  const url = `wss://${window.location.host}/${socketPath}`;
  const splittedURL = url.split("/");

  const game = {
    secretId: splittedURL[splittedURL.length - 1],
    socket: null,
    pawnStr: null,
    pawn: null,
    previewPosition: { x: 1, z: 1 },
    isMyTurn: false,
    textTurn: null,
    arena: null,
    scene: UTILS.createScene(),
    renderer: UTILS.createRenderer(),
    display: null,
    keys: {},
  };
  game.keys['ArrowUp'] = 'up'
  game.keys['ArrowDown'] = 'up'
  game.keys['ArrowLeft'] = 'up'
  game.keys['ArrowRight'] = 'up'
  game.keys[' '] = 'up'
  game.socket = new WebSocket(url);
  UTILS.createContainerForGame("TicTacToe", game.renderer);
  JS_UTILS.eraseCookie("username");
  game.arena = TIK_TAK_TOE.createArena(game.scene);
  game.display = TIK_TAK_TOE.createCamera(game.renderer, X_SIZE_MAP);
  TIK_TAK_TOE.updateTurn(game.scene, "Opponent turn", game);

  SOCKET.socketListener(game);
  windowListener(game);
  await waitPawnSelection(game);

  let lastTime = 0;
  // ------------------------------------loop------------------------------------
  function animate(currentTime) {
    if (lastTime) {
      const delta = (currentTime - lastTime) / 10;
      TIK_TAK_TOE.move(game.keys, game);
      if (game.isMyTurn) {
        TIK_TAK_TOE.printPrev(game.keys, game);
      }
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
