import { doRequest } from "../utils/fetch.js";

export const createTournamentHandler = () => {
	const handleClick = (event) => {
		if (event.target.matches("#create")) {
			let data = {
				name: document.getElementById("tour-name").value,
				nb_players: parseInt(
					document.getElementById("nb_players").value,
				),
				id_game: parseInt(document.getElementById("game_id").value),
			};
			doRequest.post(`/api/create_tournament/`, data, (data) => {
				if (data.status === "ok") {
					window.location.hash =
						"lobby-tournament?id=" + data.id_tournament;
				} else if (data.status === "error") {
					const messageElement = document.getElementById("message");
					if (!messageElement)
						return console.error(
							'Element with class "message" not found',
						);
					messageElement.textContent = data.message;
				}
			});
		}
	};

	document.body.addEventListener("click", handleClick);
	return () => document.body.removeEventListener("click", handleClick);
};
