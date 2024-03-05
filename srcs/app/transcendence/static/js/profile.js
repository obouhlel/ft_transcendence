import { doRequest } from './utils/fetch.js';

export	function	show_dynamic_stats(gameID)
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
async	function getUserDataById(userID)
{
	return fetch(`/api/get_user_by_id/${userID}`)
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

async	function getUserConnected()
{
	return fetch(`/api/get_user_connected`)
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

export async function show_dynamic_history(gameID) {
	fetch(`/api/get_user_history_by_game/${gameID}`)
	.then(response => response.json())
	.then(async data => {
		if (data.status === 'ok') {
			const tbody = document.querySelector('.Matches .table .tbody');
			if (!tbody) {
				console.error('Element with class "Matches table tbody" not found');
				return;
			}
			let html = '';
			for (const party of data.parties) {
				const adversary = await getUserDataById(party.player2);
				const userConnected = await getUserConnected();
				let score = 0;
				let party_status = 0;
				const winner_score = party.score1 > party.score2 ? party.score1 : party.score2;
				const loser_score = party.score1 < party.score2 ? party.score1 : party.score2;
				if (party.winner_party === userConnected.id)
				{
					score = `${winner_score} - ${loser_score}`;
					party_status = 'Win';
				}
				else
				{
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
		} else {
			console.error(data.message);
		}
	});
}

export async function show_dynamic_friends() {
    const userConnected = await getUserConnected();
    const userID = userConnected.id;
    fetch(`/api/get_all_friends/${userID}`)
    .then(response => response.json())
    .then(data => {
        if (data.status === 'ok') {
            const friendList = document.querySelector('.friend-list-members');
            if (!friendList) {
                console.error('Element with class "friend-list-members" not found');
                return;
            }
            document.querySelectorAll('.friend-card').forEach(card => card.remove());
            data.friends.forEach(friend => {
                const friendCard = document.createElement('div');
                friendCard.className = `friend-card ${friend.status === 'online' ? 'online-friend' : 'offline-friend'}`;
				friendCard.id = friend.id;
				const buttonClass = friend.status === 'offline' ? 'active-member-btn offline-member' : 'active-member-btn';
                friendCard.innerHTML = `
                    <div class="member-details">
						<img src="${friend.avatar || defaultAvatarUrl}" alt="">
                        <div>
                            <h2>${friend.username}</h2>
                        </div>
                    </div>
                    <button class="${buttonClass}">${friend.status}</button>
                    <i class="fa-solid fa-user-xmark delete-friend"></i>
                `;
                friendList.prepend(friendCard);
            });
        } else {
            console.error(data.message);
        }
    })
    .catch(console.error);
}

// delete friend
export async function deleteFriend()
{
	const parentElement = document.querySelector('.friend-list-members');
	if (!parentElement)
	{
		console.error('Element with class "friend-list-members" not found');
		return;
	}
	parentElement.addEventListener('click', function(event) {
		const target = event.target;
		if (!target.classList.contains('delete-friend'))
			return;
		const friendID = target.parentElement.id;
		const csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
		fetch(`/api/delete_friend/${friendID}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
		.then(response => response.json())
		.then(data => {
			if (data.status === 'ok') {
				show_dynamic_friends();
			} else {
				console.error(data.message);
			}
		}
		);
	});
}

/*ACTIVE GAME-TAB FUNCTIONALITY IN USER PROFILE*/
export function switchGameTab()
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
export async function addFriendHandler()
{
	const parentElement = document.querySelector('.find-friends-result');
	if (!parentElement)
	{
		console.error('Element with class "find-friends-result" not found');
		return;
	}
	parentElement.addEventListener('click', function(event) {
		const target = event.target;
		if (!target.classList.contains('modal-add-btn'))
			return;
		const friendID = document.querySelector('.user-row').id;
        doRequest.post(`/api/add_friend/${friendID}`, {}, data => {
            if (data.status === 'ok') {
				show_dynamic_friends();
            } else {
                console.error(data.message);
            }
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
		console.log('allFriendsBtn');
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

export function searchFunction()
{
	let searchInput = document.getElementById('search').value;
	if (!searchInput || searchInput.trim() === '')
		return;
	if (searchInput != '')
	{
		fetch(`/api/search_user/${searchInput}`)
		.then(response => response.json())
		.then(async data => {
			if (data.status === 'ok') {
				const resultContainer = document.querySelector('.find-friends-result');
				const friendCards = [];
				for (const user of data.users) {
					const	userConnected = await getUserConnected();
					const	userConnectedID = userConnected.id;
					if (user.id === userConnectedID)
						continue;
					const friendCard = document.createElement('div');
					friendCard.className = 'user-row';
					friendCard.id = user.id;
					friendCard.innerHTML = `
						<div class="user-info">
							<img src="${user.avatar || defaultAvatarUrl}" alt="">
							<span>${user.username}</span>
						</div>
						<button class="modal-add-btn">
							Send Request
						</button>
					`;
					friendCards.push(friendCard);
				}
				resultContainer.innerHTML = '';
				friendCards.forEach(friendCard => resultContainer.appendChild(friendCard));
			}
		})
		.catch(error => {
			console.error(error);
		});
	}
}

/*OPEN MODAL TO SEARCH AND ADD FRIENDS*/
export function openModal()
{
	const modal = document.querySelector('.modal');
	const overlay = document.querySelector('.overlay');
	const btnCloseModal = document.querySelector('.close-modal');
	const btnOpenModal = document.querySelector('.show-modal');

	const openModal = function () {
	document.getElementById('search').value = '';
	modal.classList.remove('hidden');
	overlay.classList.remove('hidden');
	};

	const closeModal = function () {
	modal.classList.add('hidden');
	overlay.classList.add('hidden');
	};

	btnOpenModal.addEventListener('click', openModal);
	btnCloseModal.addEventListener('click', closeModal);
	overlay.addEventListener('click', closeModal);
}
