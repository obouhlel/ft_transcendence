import { doRequest } from "../utils/fetch.js";

export async function socketTournamentHandler() {
  let socketDynamiqueTournament = new WebSocket(
    "wss://" +
      window.location.host +
      "/ws/tournament/" +
      window.location.hash.split("=")[1]
  );

  socketDynamiqueTournament.onopen = function (event) {
    console.log("###### WebSocket tournament connection opened #####");
  };

  socketDynamiqueTournament.onclose = function (event) {
    console.log("###### WebSocket tournament connection closed ######");
  };

  socketDynamiqueTournament.onmessage = async function (event) {
    let message = JSON.parse(event.data);

    // If the message is the current player count, update the display
    if (message.action === "Update Player Count") {
      let playerCount = message.playerCount;
      let maxPlayerCount = message.maxPlayerCount;
      let tournamentId = message.tournamentId;

      // Update the player count display
      let playerCountElement = document.getElementById(
        `player-count-${tournamentId}`
      );
      if (playerCountElement) {
        playerCountElement.textContent = `${playerCount}/${maxPlayerCount}`;
      }

      // update the list of player if we are in the lobby
      if (window.location.hash === `#lobby-tournament?id=${tournamentId}`) {
        let playerListElement = document.querySelector(`.players-list`);

        if (playerListElement) {
          playerListElement.innerHTML = "";
          message.users.forEach((user) => {
            let playerElement = document.createElement("div");
            playerElement.className = "player";
            playerElement.id = `player-${user.id}`;

            let imgElement = document.createElement("img");
            imgElement.src = user.avatar
              ? `${user.avatar}`
              : "/static/img/user-image.png";
            imgElement.alt = `${user.username} Avatar`;

            let pElement = document.createElement("p");
            pElement.textContent = `${user.username}`;

            playerElement.appendChild(imgElement);
            playerElement.appendChild(pElement);

            playerListElement.appendChild(playerElement);
          });
        }
      }
    } else if (message.action === "Update Tournament List") {
      const tbody = document.querySelector("tbody");
      if (tbody !== null) tbody.innerHTML = "";
      message.tournaments.forEach((tournament) => {
        const tr = document.createElement("tr");

        const tdName = document.createElement("td");
        tdName.textContent = tournament.name;
        tr.appendChild(tdName);

        const tdPlayerCount = document.createElement("td");
        tdPlayerCount.className = "player-count";
        tdPlayerCount.id = `player-count-${tournament.id}`;
        tdPlayerCount.textContent = `${tournament.users.length}/${tournament.nb_player_to_start}`;
        tr.appendChild(tdPlayerCount);

        const tdStatus = document.createElement("td");
        if (tournament.users.length === tournament.nb_player_to_start) {
          tdStatus.textContent = "Full";
        } else {
          tdStatus.textContent = tournament.status;
        }
        tr.appendChild(tdStatus);

        const tdAction = document.createElement("td");
        const aAction = document.createElement("a");
        aAction.className = "blue-btn";
        aAction.id = `join-tournament-btn-${tournament.id}`;
        aAction.textContent = "Join";
        tdAction.appendChild(aAction);
        tr.appendChild(tdAction);

        doRequest
          .get("/api/get_user_connected")
          .then((userConnected) => {
            console.log("userConnected :", userConnected);

            if (tournament.creator_id === userConnected.user.id) {
              const tdDelete = document.createElement("td");
              const aDelete = document.createElement("a");
              aDelete.className = "red-btn";
              aDelete.id = `delete-tournament-btn-${tournament.id}`;
              aDelete.textContent = "Delete";
              tdDelete.appendChild(aDelete);
              tr.appendChild(tdDelete);
            }
          })
          .catch((error) => {
            console.error("Error:", error);
          });

        if (tbody !== null) tbody.appendChild(tr);
      });
    } else if (message.action === "update page") {
      const currentHash = window.location.hash.substring(1);
      const dataPage = await doRequest.get(`/pages/${currentHash}`);
      const afterHash = window.location.hash.substring(1);
      if (currentHash !== afterHash) return;
      const pageContent = document.getElementById("page");
      pageContent.innerHTML = dataPage.html;
    }
  };

  window.addEventListener("hashchange", function () {
    const pageNoNotification = ["tournament", "lobby-tournament", "create-tournament"];
    const currentHash = window.location.hash.substring(1).split("?")[0];
    console.log(currentHash);
    if (!pageNoNotification.includes(currentHash)) {
      socketDynamiqueTournament.close();
    }
  });
}

export async function tournamentHandler() {
  const handleClick = (event) => {
    const leaveButtons = document.querySelectorAll(
      '[id^="leave-tournament-btn-"]'
    );
    if (event.target.matches('[id^="join-tournament-btn-"]')) {
      if (leaveButtons.length > 0) {
        console.error("Invalid button clicked");
        const messageElement = document.getElementById("message");
        if (!messageElement)
          return console.error('Element with id "message" not found');
        messageElement.textContent = "You can only one join a tournament";
        return;
      }
      let tournamentId = event.target.id.split("-")[3];
      let data = { id_tournament: tournamentId };
      doRequest.post(`/api/join_tournament/`, data, (response_data) => {
        console.log(response_data);
        if (response_data.status === "ok")
          window.location.hash = "lobby-tournament?id=" + tournamentId;
        else if (response_data.status === "error") {
          const messageElement = document.getElementById("message");
          if (!messageElement)
            return console.error('Element with id "message" not found');
          messageElement.textContent = response_data.message;
        }
      });
    } else if (event.target.matches('[id^="leave-tournament-btn-"]')) {
      let tournamentId = event.target.id.split("-")[3];
      let data = { id_tournament: tournamentId };
      doRequest.post(`/api/leave_tournament/`, data, (response_data) => {
        console.log(response_data);
      });
    } else if (event.target.matches('[id^="delete-tournament-btn-"]')) {
      let tournamentId = event.target.id.split("-")[3];
      doRequest.delete(
        `/api/delete_tournament/${tournamentId}/`,
        {},
        (response_data) => {
          console.log(response_data);
        }
      );
    }
  };
  document.body.addEventListener("click", handleClick);
  return () => document.body.removeEventListener("click", handleClick);
}

export const createTournamentHandler = () => {
  const handleClick = (event) => {
    if (event.target.matches("#create")) {
      let data = {
        name: document.getElementById("tour-name").value,
        nb_players: parseInt(document.getElementById("nb_players").value),
        id_game: parseInt(document.getElementById("game_id").value),
      };
      doRequest.post(`/api/create_tournament/`, data, (data) => {
        console.log(data);
        if (data.status === "ok") {
          window.location.hash = "lobby-tournament?id=" + data.id_tournament;
        } else if (data.status === "error") {
          const messageElement = document.getElementById("message");
          if (!messageElement)
            return console.error('Element with class "message" not found');
          messageElement.textContent = data.message;
        }
      });
    }
  };

  document.body.addEventListener("click", handleClick);
  return () => document.body.removeEventListener("click", handleClick);
};

export function aliasFormsHandler() {
  const aliasForms = document.getElementById("alias-forms");
  if (!aliasForms)
    return console.error('Element with id "alias-forms" not found');
  const handleSubmit = (event) => {
    event.preventDefault();

    const alias = document.getElementById("alias").value;
    const data = { alias: alias };
    doRequest.post(`/api/alias/`, data, (response) => {
      console.log(response);
      const messageElement = document.getElementById("message");
      if (!messageElement)
        return console.error('Element with class "message" not found');
      if (response.status === "ok") {
        messageElement.textContent = response.message;
      } else if (response.status === "error") {
        messageElement.textContent = response.message;
      }
    });
  };
  aliasForms.addEventListener("submit", handleSubmit);
}

export async function tournamentLobbyHandler() {
  const tournamentId = window.location.hash.split("id=")[1];
  const hashage = window.location.hash.split("?")[0];
  console.log("Tournament id: ", tournamentId);
  const data = await doRequest.get(`/api/get_tournament_by_id/${tournamentId}`);
  console.log(data);
  const messageElement = document.getElementById("message");
  if (!messageElement)
    return console.error('Element with id "message" not found');
  if (data.status === "error") {
    messageElement.textContent = data.message;
    return;
  }
  const tournament = data.tournament;
  const nb_players = tournament.users.length;
  const nb_players_max = tournament.nb_player_to_start;
  console.log("Nb players: ", nb_players);
  console.log("Nb players max: ", nb_players_max);
  console.log("Tournament: ", tournament);
  const handleClickStart = (event) => {
    if (nb_players === nb_players_max) {
      messageElement.textContent = "Starting the tournament...";
      // RUN WEBSOCKET
    } else {
      messageElement.textContent = "Need more players to start the tournament";
    }
  };
  const handleClickLeave = (event) => {
    const gameId = tournament.id_game;
    doRequest.post(
      `/api/leave_tournament/`,
      { id_tournament: tournamentId },
      (response) => {
        console.log(response);
        if (response.status === "ok")
          window.location.hash = "tournament?id=" + gameId;
        else if (response.status === "error") {
          messageElement.textContent = response.message;
        }
      }
    );
  };
  const handleHashChange = (event) => {
    const newHash = window.location.hash.split("?")[0];
    if (
      newHash !== "#lobby-tournament" &&
      newHash !== "#tournament" &&
      newHash !== "#create-tournament"
    ) {
      const data = { id_tournament: tournamentId };
      console.log(
        "------------------ Leaving tournament on hash change + data: ",
        data
      );
      doRequest.post(`/api/leave_tournament/`, data, (response) => {
        console.log("------------------ response: ", response);
      });
    }
  };

  const handleLoad = (event) => {
    const currentHash = window.location.hash.split("?")[0];
    if (currentHash === "#lobby-tournament") {
      const data = { id_tournament: tournamentId };
      doRequest.post(`/api/join_tournament/`, data);
    }
  };
  window.addEventListener("hashchange", handleHashChange);
  window.addEventListener("load", handleLoad);
  const startButton = document.getElementById("start-tournament");
  if (startButton) startButton.addEventListener("click", handleClickStart);
  const leaveButton = document.getElementById("leave-tournament");
  if (leaveButton) leaveButton.addEventListener("click", handleClickLeave);
}
