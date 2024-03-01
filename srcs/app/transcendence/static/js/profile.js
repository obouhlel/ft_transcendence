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

export	function show_dynamic_history(gameID) {
    fetch(`/api/get_user_history_by_game/${gameID}`)
    .then(response => response.json())
    .then(async data => {
        if (data.status === 'ok') {
            const tbody = document.querySelector('.Matches .table .tbody');
            if (!tbody)
                console.error('Element with class "Matches table tbody" not found');
            tbody.innerHTML = '';
            for (const party of data.parties) {
                const tr = document.createElement('div');
                tr.className = 'tr';

                const td1 = document.createElement('div');
                const adversary = await getUserDataById(party.player2);
                td1.className = 'td data-one';
                td1.textContent = adversary ? adversary.username : 'Unknown';
                tr.appendChild(td1);

                const td2 = document.createElement('div');
                const score = party.score1 + ' - ' + party.score2;
                td2.className = 'td data-two';
                td2.textContent = score;
                tr.appendChild(td2);

				if (party.score1 > party.score2)
					tr.style.backgroundColor = 'rgba(0, 255, 0, 0.2)';
				else if (party.score1 < party.score2)
					tr.style.backgroundColor = 'rgba(255, 0, 0, 0.2)';

                const td3 = document.createElement('div');
                td3.className = 'td data-three';
                td3.textContent = new Date(party.ended_at).toLocaleDateString();
                tr.appendChild(td3);

                const td4 = document.createElement('div');
                td4.className = 'td data-four';
                td4.textContent = party.status;
                tr.appendChild(td4);

                tbody.appendChild(tr);
            }
        } else {
            console.error(data.message);
        }
    })
    .catch(error => {
        console.error(error);
    });
}

export async	function show_dynamic_friends() {
	const	userConnected = await getUserConnected();
	const	userID = userConnected.id;
    fetch(`/api/get_all_friends/${userID}`)
    .then(response => response.json())
    .then(data => {
        if (data.status === 'ok') {
            const friendList = document.querySelector('.friend-list-membersdsds');
            if (!friendList) {
				console.error('Element with class "friend-list-members" not found');
                return;
            }
			const friendCards = document.querySelectorAll('.friend-card.online-friend');
            friendCards.forEach((card) => {
				card.remove();
			});
            data.friends.forEach((friend) => {
                const friendCard = document.createElement('div');
                friendCard.className = `friend-card ${friend.status === 'Online' ? 'online-friend' : 'offline-friend'}`;

                const memberDetails = document.createElement('div');
                memberDetails.className = 'member-details';

                const img = document.createElement('img');
                img.src = friend.avatar || '{% static "img/user-image-s.png" %}';
                img.alt = '';

                const div = document.createElement('div');
                const h2 = document.createElement('h2');
                h2.textContent = friend.username;
                div.appendChild(h2);

                memberDetails.appendChild(img);
                memberDetails.appendChild(div);

                const activeMemberBtn = document.createElement('button');
                activeMemberBtn.className = 'active-member-btn';
                activeMemberBtn.textContent = friend.status;

                const i = document.createElement('i');
                i.className = 'fa-solid fa-user-xmark';

                friendCard.appendChild(memberDetails);
                friendCard.appendChild(activeMemberBtn);
                friendCard.appendChild(i);

                friendList.appendChild(friendCard);
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

export function addFriend()
{
	const addFriendBtn = document.querySelector('.add-friend');
	if (!addFriendBtn)
	{
		console.error('Element with class "add-friend" not found');
		return;
	}
	addFriendBtn.addEventListener('click', function() {
		const userConnected = getUserConnected();
		const userID = userConnected.id;
		const friendID = this.getAttribute('data-id');
		fetch(`/api/add_friend/${userID}/${friendID}`)
		.then(response => response.json())
		.then(data => {
			if (data.status === 'ok') {
				console.log('Friend added');
			} else {
				console.error(data.message);
			}
		})
		.catch(error => {
			console.error(error);
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
