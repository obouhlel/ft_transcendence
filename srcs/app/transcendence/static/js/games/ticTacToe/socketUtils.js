import * as JS_UTILS from "../jsUtils.js";
import * as TIK_TAK_TOE from "./ticTacToeUtils.js";

import { getPawn } from "./ticTacToeUtils.js";

import { PawnCross, PawnCircle } from "./class/Pawn.js";

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

export function sendNewPawnPosition(game, x, z) {
  let message = {
    game: "position",
    id: game.secretId,
    username: game.username,
    x: x,
    y: z,
  };
  JS_UTILS.sendMessageToSocket(game.socket, message);
}

function parseMessage(data, game) {
  if ("game" in data) {
    if (data["game"] == "starting") {
      game.pawnStr = data["pawn"];
      game.pawn = getPawn(game);
    }
    if (data["game"] == "play") {
      game.isMyTurn = true;
      TIK_TAK_TOE.updateTurn(game.scene, "Your turn", game);
    }
    if (data["game"] == "position") {
      let pawn = null;
      if (game.pawnStr == "O") {
        pawn = new PawnCross(game, 0, 0);
      } else if (game.pawnStr == "X") {
        pawn = new PawnCircle(game, 0, 0);
      }
      pawn.cube.position.x = game.arena[data["x"]][data["z"]].floor.position.x;
      pawn.cube.position.z = game.arena[data["x"]][data["z"]].floor.position.z;
      game.arena[data["x"]][data["z"]].pawnOnThis = pawn;
    }
    if (data["game"] == "end") {
      if (data["winner"] == game.username) {
        TIK_TAK_TOE.updateTurn(game.scene, "You Win", game);
      } else if (data["winner"] == "draw") {
        TIK_TAK_TOE.updateTurn(game.scene, "  Draw  ", game);
      } else {
        TIK_TAK_TOE.updateTurn(game.scene, "You Lose", game);
      }
      game.socket.close();
      game.isMyTurn = false;
      openWinnerModal(data["winner"], data["type"]);
      setTimeout(() => {
        window.location.hash = "home";
      }, 3000);
    }
  }
  else if ("error" in data) {
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

  game.socket.onclose = function () {
  };

  game.socket.onerror = function (error) {
    // console.error(error);
  };
}
