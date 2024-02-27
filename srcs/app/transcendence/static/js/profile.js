export function show_dynamic_profile()
{
	return fetch('/api/get_all_games/')
	.then(response => response.json())
	.then(data => {
		if (data.status === 'ok') {
			const navs = document.querySelector('.navs');
			if (!navs) {
				console.error('Element with class "navs" not found');
				return;
			}
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
				show_dynamic_stats(game.id);
				show_dynamic_history(game.id);
			});
		}
		else {
			console.error(data.message);
		}
	});
}

function	show_dynamic_stats(gameID)
{
	if (!gameID)
	{
		const tabId = this.getAttribute('data-tab');
		if (!tabId)
			console.error('No tab ID class "data-tab" not found');
		gameID = tabId.slice(3);
	}
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

// ! utiliser doRequest.GET de ous apres merge
function getUserDataById(userID)
{
	fetch(`/api/get_user/${userID}`)
	.then(response => response.json())
	.then(data => {
		if (data.status === 'ok') {
			return data.user;
		} else {
			console.error(data.message);
			return null;
		}
	})
	.catch(error => {
		console.error(error);
		return null;
	});
}

function getUserConnected()
{
	fetch(`/api/get_user_connected`)
	.then(response => response.json())
	.then(data => {
		if (data.status === 'ok') {
			return data.user;
		} else {
			console.error(data.message);
			return null;
		}
	})
	.catch(error => {
		console.error(error);
		return null;
	});

}

function show_dynamic_history(gameID) {
    fetch(`/api/get_user_history_by_game/${gameID}`)
    .then(response => response.json())
    .then(data => {
        if (data.status === 'ok') {
			console.log("data HISTORY: ", data);
            const tbody = document.querySelector('.Matches .table .tbody');
			if (!tbody)
				console.error('Element with class "Matches table tbody" not found');
            tbody.innerHTML = ''; // Supprime les anciennes lignes
            data.parties.forEach(party => {
                const tr = document.createElement('div');
                tr.className = 'tr';

                const td1 = document.createElement('div');
				const adversary = getUserDataById(party.player2);
                td1.className = 'td data-one';
                td1.textContent = 'Unknown';
                tr.appendChild(td1);

                const td2 = document.createElement('div');
                td2.className = 'td data-two';
                td2.textContent = party.score;
                tr.appendChild(td2);

                const td3 = document.createElement('div');
                td3.className = 'td data-three';
                td3.textContent = party.date;
                tr.appendChild(td3);

                const td4 = document.createElement('div');
                td4.className = 'td data-four';
                td4.textContent = party.status;
                tr.appendChild(td4);

                tbody.appendChild(tr);
            });
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
			show_dynamic_history(gameID);
        });
    });
}

/*FRIENDS BUTTONS FUNCTIONALITY*/
export function friendsTab()
{
	function filterFriends(displayOnline, displayOffline) {
		const onlineFriends = document.querySelectorAll('.online-friend');
		const offlineFriends = document.querySelectorAll('.offline-friend');

		onlineFriends.forEach(friend => {
		friend.style.display = displayOnline ? '' : 'none';
		});

		offlineFriends.forEach(friend => {
		friend.style.display = displayOffline ? '' : 'none';
		});
	}

	function updateButtonStyles(activeButton) {
		const buttons = document.querySelectorAll('.categories-btns ul li button');
		buttons.forEach(button => {
		if (button === activeButton) {
			button.classList.add('c-btn-active');
		} else {
			button.classList.remove('c-btn-active');
		}
		});
	}

	const allFriendsBtn = document.querySelector('.all-friends-btn');
	const onlineFriendsBtn = document.querySelector('.online-friends-btn');
	const offlineFriendsBtn = document.querySelector('.offline-friends-btn');


	allFriendsBtn.addEventListener('click', function() {
		filterFriends(true, true);
		updateButtonStyles(this); // 'this' refers to the clicked button
	});
	onlineFriendsBtn.addEventListener('click', function() {
		filterFriends(true, false);
		updateButtonStyles(this);
	});
	offlineFriendsBtn.addEventListener('click', function() {
		filterFriends(false, true);
		updateButtonStyles(this);
	});
}
