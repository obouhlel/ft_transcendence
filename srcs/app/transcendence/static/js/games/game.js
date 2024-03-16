import {
  connectWebsocketMatchmacking,
  sendMatchmakingLeave,
  sendMatchmakingJoin,
} from "./matchmaking.js";

export function GameHandler() {
  connectWebsocketMatchmacking();
  const handleClick = (event) => {
    if (event.target.matches(".matchmaking-btn")) {
      if (event.target.innerHTML === "Matchmaking") {
        console.log("matchmaking");
        let data = { gameId: event.target.dataset.gameId };
        sendMatchmakingJoin(window.socketMatchmaking, data);
      }
      if (event.target.innerHTML === "Cancel matchmaking") {
        console.log("cancel matchmaking");
        let data = { gameId: event.target.dataset.gameId };
        sendMatchmakingLeave(window.socketMatchmaking, data);
      }
    }
  };
  document.body.addEventListener("click", handleClick);
  return () => document.body.removeEventListener("click", handleClick);
}
