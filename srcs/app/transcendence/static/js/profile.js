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

/*ACTIVE GAME-TAB FUNCTIONALITY IN USER PROFILE*/
export function gameTab()
{
	document.querySelectorAll('.tab-link').forEach(function(link) {
		link.addEventListener('click', function(e) {
			e.preventDefault();

			const tabId = this.getAttribute('data-tab');

			document.querySelectorAll('.tab-link').forEach(function(link) {
				link.classList.remove('active');
			});

			this.classList.add('active');

			document.querySelectorAll('.tab-content').forEach(function(tab) {
				tab.classList.remove('active-tab');
			});

			document.getElementById(tabId).classList.add('active-tab');
		});
	});
}

/*FRIENDS BUTTONS FUNCTIONALITY*/
export function friendsTab()
{
	document.addEventListener('DOMContentLoaded', function() {
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
	  });
}