import * as JS_UTILS from "../jsUtils.js";
import * as UTILS from "./pongUtils.js";
import * as PONG from "./pongUtils.js";

import { openVersusModal, openWinnerModal } from "../game-info.js";

function sendStartingGame(game) {
  let message = {
    game: "starting",
    id: game.secretId,
    username: game.username,
  };
  openVersusModal();
  setTimeout(() => {
    JS_UTILS.sendMessageToSocket(game.socket, message);
  }, 5000);
}

export function sendLeaveGame(game) {
  let message = {
    game: "leaved",
    id: game.secretId,
    username: game.username,
  };
  JS_UTILS.sendMessageToSocket(game.socket, message);
}

export function sendPlayerPosition(player, game) {
  let message = {
    game: "player position",
    id: game.secretId,
    username: game.username,
    position: player.cube.position.z,
  };
  JS_UTILS.sendMessageToSocket(game.socket, message);
}

function parseMessage(message, game) {
  if ("game" in message) {
    if (message["game"] == "starting") {
      game.side = message["side"];
    }
    if (message["game"] == "positions") {
      if (game.side == "left") game.enemyPosition = message["playerRight"];
      else if (game.side == "right") game.enemyPosition = message["playerLeft"];
      game.ballPosition.x = message["positionBallX"];
      game.ballPosition.z = message["positionBallZ"];
    }
    if (message["game"] == "score") {
      PONG.updateScore(game.scene, message["score"], game);
      game.playerLocal.reset();
    }
    if (message["game"] == "end") {
      game.needStop = true;
      if (message["winner"] == message["username"]) {
        UTILS.updateScore(game.scene, "You win", game);
      } else {
        UTILS.updateScore(game.scene, "You lose", game);
      }
      setTimeout(() => {
        openWinnerModal(message["winner"]);
      }, 3000);
      setTimeout(() => {
        window.location.hash = "home";
      }, 3000);
    }
  }
}

export function socketListener(game) {
  game.socket.onopen = function () {
    console.log("Connection established");
    sendStartingGame(game);
  };

  game.socket.onmessage = function (e) {
    let data = JSON.parse(e.data);
    console.log("Received message: " + e.data);
    parseMessage(data, game);
  };

  game.socket.onclose = function () {
    console.log("Connection closed");
  };

  game.socket.onerror = function (error) {
    console.log(`socket error: ${error}`);
    console.error(error);
  };
}
