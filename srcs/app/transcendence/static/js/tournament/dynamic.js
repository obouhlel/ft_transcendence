import { doRequest } from "../utils/fetch.js";

export async function socketTournamentHandler() {
	let socketDynamiqueTournament = new WebSocket(
		"wss://" +
			window.location.host +
			"/ws/tournament/" +
			window.location.hash.split("=")[1],
	);

	socketDynamiqueTournament.onopen = function (event) {};

	socketDynamiqueTournament.onclose = function (event) {};

	socketDynamiqueTournament.onmessage = async function (event) {
		let message = JSON.parse(event.data);

		// If the message is the current player count, update the display
		if (message.action === "Update Player Count") {
			let playerCount = message.playerCount;
			let maxPlayerCount = message.maxPlayerCount;
			let tournamentId = message.tournamentId;

			// Update the player count display
			let playerCountElement = document.getElementById(`player-count-${tournamentId}`);
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
							? `/media/${user.avatar}`
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
		}
		else if (message.action === "Update Tournament List") {
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

				if (tbody !== null) tbody.appendChild(tr);
			});
		}
	};

	window.addEventListener("hashchange", (event) => {
		const hash = window.location.hash.split("?")[0];
		if (hash !== "#lobby-tournament" && hash !== "#tournament" && hash !== "#create-tournament") {
			socketDynamiqueTournament.close();
		}
	});
}
