import { doRequest } from '../utils/fetch.js';

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

export async function show_dynamic_friends() {
    const data = await doRequest.get('/api/get_user_connected');
	const userConnected = data.user;
    const userID = userConnected.id;
    fetch(`/api/get_all_friends/${userID}`)
    .then(response => response.json())
    .then(data => {
        if (data.status === 'ok') {
            const friendList = document.querySelector('.friend-list-members');
            if (!friendList) {
                console.error('Element with class "friend-list-members" not found');
                return ;
            }
            document.querySelectorAll('.friend-card').forEach(card => card.remove());
            data.friends.forEach(friend => {
                const friendCard = document.createElement('div');
                friendCard.className = `friend-card ${friend.status === 'online' ? 'online-friend' : 'offline-friend'}`;
				friendCard.id = friend.id;
                friendCard.innerHTML = `
                    <div class="member-details">
						<img src="${friend.avatar || defaultAvatarUrl}" alt="">
                        <div>
                            <h2>${friend.username}</h2>
                        </div>
                    </div>
                    <button class="active-member-btn">${friend.status}</button>
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
		return ;
	}
	parentElement.addEventListener('click', function(event) {
		const target = event.target;
		if (!target.classList.contains('delete-friend'))
			return;
		const friendID = target.parentElement.id;
        doRequest.delete(`/api/delete_friend/${friendID}`, show_dynamic_friends);
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
					const	userConnected = await doRequest.get('/api/get_user_connected');
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
            }
			else {
                console.error(data.message);
            }
        });
	});
}