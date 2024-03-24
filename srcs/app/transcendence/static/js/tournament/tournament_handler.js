import { doRequest } from "../utils/fetch.js";

export async function tournamentHandler() {
	const handleClick = (event) => {
		const leaveButtons = document.querySelectorAll('[id^="leave-tournament-btn-"]');

		if (event.target.matches('[id^="join-tournament-btn-"]')) {

			if (leaveButtons.length > 0) {
				// console.error("Invalid button clicked");
				const messageElement = document.getElementById("message");
				if (!messageElement)
					return;
					// return console.error('Element with id "message" not found');
				messageElement.textContent =
					"You can only one join a tournament";
				return ;
			}

			let tournamentId = event.target.id.split("-")[3];
			let data = { id_tournament: tournamentId };

			doRequest.post(`/api/join_tournament/`, data, (response_data) => {
				if (response_data.status === "ok")
					window.location.hash = "lobby-tournament?id=" + tournamentId;
				else if (response_data.status === "error") {
					const messageElement = document.getElementById("message");
					if (!messageElement)
						return;
						// return console.error('Element with id "message" not found');
					messageElement.textContent = response_data.message;
				}
			});
		}
		else if (event.target.matches('[id^="leave-tournament-btn-"]')) {
			let tournamentId = event.target.id.split("-")[3];
			let data = { id_tournament: tournamentId };
			doRequest.post(`/api/leave_tournament/`, data);
		}
	};

	document.body.addEventListener("click", handleClick);
	return () => document.body.removeEventListener("click", handleClick);
}
