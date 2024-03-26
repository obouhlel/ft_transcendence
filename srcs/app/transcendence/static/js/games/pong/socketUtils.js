import * as JS_UTILS from "../jsUtils.js";
import * as UTILS from "./pongUtils.js";
import * as PONG from "./pongUtils.js";

import { openVersusModal, openWinnerModal } from "../game-info.js";

function sendStartingGame(game) {
  const hashQuery = new URLSearchParams(window.location.hash.split('?')[1]);
  const party_id = hashQuery.get('party_id');
  let message = {
    game: "starting",
    id: game.secretId,
    username: game.username,
    party_id: party_id,
  };
  openVersusModal();
  setTimeout(() => {
    JS_UTILS.sendMessageToSocket(game.socket, message);
  }, 3000);
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
      game.socket.close();
      openWinnerModal(message["winner"], message["type"]);
      if (message["type"] == "Matchmaking") {

        setTimeout(() => {
          window.location.hash = "home";
        }, 3000);
      }
      else if (message["type"] == "Tournament") {
        if (message["status"] == "finished") {
          setTimeout(() => {
            window.location.hash = "home";
          }, 3000);
        }
        else if (message["winner"] == message["username"]) {
          console.log("Waiting for next round");
        }
        else {
          setTimeout(() => {
            window.location.hash = "home";
          }, 3000);
        }
      }
    }
  } else if ("error" in message) {
    window.location.hash = "home";
  }
}

export function socketListener(game) {
  game.socket.onopen = function () {
    sendStartingGame(game);
  };

  game.socket.onmessage = function (e) {
    let data = JSON.parse(e.data);
    parseMessage(data, game);
  };

  game.socket.onclose = function () {};

  game.socket.onerror = function (error) {
    // console.error(error);
  };
}
