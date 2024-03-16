import { doRequest } from "../utils/fetch.js";
import { matchmacking } from "./matchmaking.js";

export function GameHandler() {
  const RoomHandler = (response_data) => {
    if (response_data["status"] === "ok") {
      console.log(response_data);
      switch (response_data["id_game"]) {
        case 1:
          matchmacking("pong");
          break;
        case 2:
          matchmacking("pong");
          break;
        default:
          console.log("error");
      }
      // show waiting for opponent
      console.log("this should redirect to the game page");
    } else {
      console.log("error");
    }
  };
  const handleClick = (event) => {
    if (event.target.matches(".matchmaking-btn")) {
      console.log("matchmaking");
      let data = { id_game: event.target.dataset.gameId };
      matchmacking(event.target.dataset.gameId);
      // doRequest.post(`/api/join_lobby/`, data, (response_data) => {
      // 	RoomHandler(response_data);
      // });
    }
  };
  document.body.addEventListener("click", handleClick);
  return () => document.body.removeEventListener("click", handleClick);
}
