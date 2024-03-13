import { doRequest } from '../utils/fetch.js';

export async function show_dynamic_stats(gameID) {
	if (!gameID) {
		const tabId = this.getAttribute('data-tab');
		if (!tabId) {
			console.error('No tab ID class "data-tab" not found');
			return;
		}
		gameID = tabId.slice(3);
	}
	try {
		const response = await fetch(`/api/get_stats_users_by_game/${gameID}`);
		const data = await response.json();
		if (data.status === 'ok') {
			const cards = document.querySelectorAll('.card h1');
			cards[0].textContent = data.stat.nb_win;
			cards[1].textContent = data.stat.nb_lose;
			cards[2].textContent = (data.stat.nb_win + data.stat.nb_lose === 0) ? 0 : (data.stat.nb_win / (data.stat.nb_win + data.stat.nb_lose)).toFixed(2);
			cards[3].textContent = data.stat.nb_played;
		}
		else {
			console.error(data.message);
		}
	}
	catch (error) {
		console.error("Can't fetch stats users, because not logged in");
	}
}

export async function show_dynamic_history(gameID) {
	try {
		const response = await fetch(`/api/get_user_history_by_game/${gameID}`);
		const data = await response.json();
		if (data.status === 'ok') {
			const tbody = document.querySelector('.Matches .table .tbody');
			if (!tbody) {
				console.error('Element with class "Matches table tbody" not found');
				return;
			}
			let html = '';
			for (const party of data.parties) {
				const data_adversary = await doRequest.get(`/api/get_user_by_id/${party.player2}`);
				const adversary = data_adversary.user;
				const data_userConnected = await doRequest.get('/api/get_user_connected');
				const userConnected = data_userConnected.user;
				let score = 0;
				let party_status = 0;
				const winner_score = party.score1 > party.score2 ? party.score1 : party.score2;
				const loser_score = party.score1 < party.score2 ? party.score1 : party.score2;
				if (party.winner_party === userConnected.id) {
					score = `${winner_score} - ${loser_score}`;
					party_status = 'Win';
				}
				else {
					score = `${loser_score} - ${winner_score}`;
					party_status = 'Lose';
				}
				const date = new Date(party.ended_at).toLocaleDateString();
				const color = party_status === 'Win' ? 'rgba(0, 255, 0, 0.2)' : 'rgba(255, 0, 0, 0.2)';

				html += `
					<div class="tr" style="background-color: ${color}">
						<div class="td data-one">${adversary ? adversary.username : 'Unknown'}</div>
						<div class="td data-two">${score}</div>
						<div class="td data-three">${date}</div>
						<div class="td data-four">${party_status}</div>
					</div>
				`;
			}
			tbody.innerHTML = html;
		}
		else {
			console.error(data.message);
		}
	}
	catch (error) {
		console.error("Can't fetch history, because not logged in");
	}
}
