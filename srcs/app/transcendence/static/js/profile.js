import { SERVER_URL, doRequest } from './fetch.js';

export function handleEditProfileFormSubmit() {
	const form = document.getElementById('profile-form');
	if (!form) { return; }
	form.addEventListener('submit', function(event) {
		event.preventDefault();

		const fields = ['username', 'firstname', 'lastname', 'email', 'password', 'password_confirm', 'avatar', 'birthdate', 'sexe'];

		let data = new FormData();
		fields.forEach(field => {
			let element = document.getElementById(field);
			if (element) {
				let value = field === 'avatar' ? element.files[0] : element.value;
				data.append(field, value);
			} else {
				console.log(`Element with ID ${field} not found`);
			}
		});

		console.log("data edit: ", Object.fromEntries(data.entries()));

		doRequest.Fetch(`${SERVER_URL}/api/edit_profile/`, 'POST', data, doRequest.callbackProfile);
	});
};

export function show_dynamic_profile()
{
	return fetch('/api/get_all_games/')
	.then(response => response.json())
	.then(data => {
		if (data.status === 'ok') {
			const navs = document.querySelector('.navs');
			navs.innerHTML = '';  // Supprime les anciens liens
			data.games.forEach((game, index) => {
				const link = document.createElement('a');
				link.className = 'tab-link';
				link.dataset.tab = `tab${game.id}`;
				link.textContent = game.name.charAt(0).toUpperCase() + game.name.slice(1);
				if (index === 0) {
					link.classList.add('active');
				}
				navs.appendChild(link);
			});
		}
		else {
			console.error(data.message);
		}
	});
}

function	show_dynamic_stats(gameID)
{
	fetch(`/api/get_stats_users_by_game/${gameID}`)
	.then(response => response.json())
	.then(data => {
		console.log("data: ", data);
		if (data.status === 'ok') {
			document.querySelector('.card:nth-child(1) h1').textContent = data.stat.nb_win;
			document.querySelector('.card:nth-child(2) h1').textContent = data.stat.nb_lose;
			if (data.stat.nb_win + data.stat.nb_lose === 0)
				document.querySelector('.card:nth-child(3) h1').textContent = 0;
			else
				document.querySelector('.card:nth-child(3) h1').textContent = (data.stat.nb_win / (data.stat.nb_win + data.stat.nb_lose)).toFixed(2);
			document.querySelector('.card:nth-child(4) h1').textContent = data.stat.nb_played;
		} else {
			console.error(data.message);
		}
	})
	.catch(error => {
		console.error(error);
	});
}

/*ACTIVE GAME-TAB FUNCTIONALITY IN USER PROFILE*/
export function gameTab()
{
    // if (!document.querySelector('.tab-link')) { setTimeout(gameTab, 500); return; }
    document.querySelectorAll('.tab-link').forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault(); // Prevent default anchor behavior

            // Get the tab ID from data-tab attribute
            const tabId = this.getAttribute('data-tab');

            // Remove active class from all tab links
            document.querySelectorAll('.tab-link').forEach(function(link) {
                link.classList.remove('active');
            });

            // Add active class to the current tab link
            this.classList.add('active');

            // Fetch game stats
            const gameID = tabId.slice(3);
			show_dynamic_stats(gameID);
        });
    });
}
