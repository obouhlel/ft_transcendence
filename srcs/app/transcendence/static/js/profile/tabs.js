import { doRequest } from '../utils/fetch.js';
import { show_dynamic_stats, show_dynamic_history } from './stats.js';

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
		}
		else {
			button.classList.remove('c-btn-active');
		}
		});
	}

	const allFriendsBtn = document.querySelector('.all-friends-btn');
	const onlineFriendsBtn = document.querySelector('.online-friends-btn');
	const offlineFriendsBtn = document.querySelector('.offline-friends-btn');
	if (!allFriendsBtn || !onlineFriendsBtn || !offlineFriendsBtn) {
		// console.error('One or more buttons not found');
		return;
	}

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