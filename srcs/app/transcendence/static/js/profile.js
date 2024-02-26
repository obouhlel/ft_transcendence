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