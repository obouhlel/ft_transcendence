import * as JS_UTILS from "./jsUtils.js";
// ----------------- Send functions -----------------

export function sendMatchmakingJoin(socket, infos) {
  const message = {
    matchmaking: "join",
    gameId: infos["gameId"],
  };
  JS_UTILS.sendMessageToSocket(socket, message);
}

export function sendMatchmakingLeave(socket, infos) {
  const message = {
    matchmaking: "leave",
    gameId: infos["gameId"],
  };
  JS_UTILS.sendMessageToSocket(socket, message);
}

function parseMessage(message, infos) {
  if ("matchmaking" in message) {
    const button = document.querySelector(".matchmaking-btn");
    if (message["matchmaking"] == "waitlist joined") {
      button.innerHTML = "Cancel matchmaking";
    } else if (message["matchmaking"] == "waitlist leaved") {
      button.innerHTML = "Matchmaking";
    } else if (message["matchmaking"] == "match found") {
      JS_UTILS.createCookie("url", message["url"], 1);
      window.location.hash = message["game"];
    }
  }
}

// ----------------- Listeners -----------------
function socketListener(socket) {
  socket.onmessage = function (e) {
    let data = JSON.parse(e.data);
    console.log("Received message: " + e.data);
    parseMessage(data);
  };

  socket.onclose = function () {
    console.log("Connection closed");
  };

  socket.onerror = function (error) {
    console.log(`socketMatchmaking error: ${error}`);
    console.error(error);
  };
}

function windowListener(socket, infos, btn) {
  window.addEventListener("hashchange", function () {
    if (socket.readyState == 1) {
      socket.close();
      window.socketMatchmaking = null;
    }
  });

  window.addEventListener("beforeunload", function () {
    if (socket.readyState == 1) {
      socket.close();
      window.socketMatchmaking = null;
    }
  });
}

export async function connectWebsocketMatchmacking() {
  const url = `wss://${window.location.host}/ws/matchmaking/`;
  window.socketMatchmaking = new WebSocket(url);
  socketListener(socketMatchmaking);
  windowListener(socketMatchmaking);
}
