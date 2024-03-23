import { doRequest } from "../utils/fetch.js";

export async function tournamentLobbyHandler() {
	// const tournamentId = window.location.hash.split("id=")[1];
	// const hashage = window.location.hash.split("?")[0];

	// const data = await doRequest.get(`/api/get_tournament_by_id/${tournamentId}`);

	// const messageElement = document.getElementById("message");
	// if (!messageElement)
	// 	return console.error('Element with id "message" not found');
	// if (data.status === "error") {
	// 	messageElement.textContent = data.message;
	// 	return ;
	// }

	// const tournament = data.tournament;
	// const nb_players = tournament.users.length;
	// const nb_players_max = tournament.nb_player_to_start;

	// const handleClickStart = (event) => {
	// 	if (nb_players === nb_players_max) {
	// 		messageElement.textContent = "Starting the tournament...";
	// 		// RUN WEBSOCKET
	// 	} else {
	// 		messageElement.textContent =
	// 			"Need more players to start the tournament";
	// 	}
	// };

	// const handleClickLeave = (event) => {
	// 	const gameId = tournament.id_game;
	// 	doRequest.post(
	// 		`/api/leave_tournament/`,
	// 		{ id_tournament: tournamentId },
	// 		(response) => {
	// 			if (response.status === "ok")
	// 				window.location.hash = "tournament?id=" + gameId;
	// 			else if (response.status === "error") {
	// 				messageElement.textContent = response.message;
	// 			}
	// 		},
	// 	);
	// };

	// const handleHashChange = (event) => {
	// 	const newHash = window.location.hash.split("?")[0];
	// 	if (
	// 		newHash !== "#lobby-tournament" &&
	// 		newHash !== "#tournament" &&
	// 		newHash !== "#create-tournament"
	// 	) {
	// 		const data = { id_tournament: tournamentId };
	// 		doRequest.post(`/api/leave_tournament/`, data);
	// 	}
	// };

	// const handleLoad = (event) => {
	// 	const currentHash = window.location.hash.split("?")[0];
	// 	if (currentHash === "#lobby-tournament") {
	// 		const data = { id_tournament: tournamentId };
	// 		doRequest.post(`/api/join_tournament/`, data);
	// 	}
	// };

	// window.addEventListener("hashchange", handleHashChange);
	// window.addEventListener("load", handleLoad);

	// const startButton = document.getElementById("start-tournament");
	// if (startButton) startButton.addEventListener("click", handleClickStart);
	// const leaveButton = document.getElementById("leave-tournament");
	// if (leaveButton) leaveButton.addEventListener("click", handleClickLeave);
}
