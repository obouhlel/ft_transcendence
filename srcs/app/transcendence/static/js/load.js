import { handleLoginFormSubmit } from './form/login.js';
import { handleRegisterFormSubmit } from './form/register.js';
import { handleEditProfileFormSubmit } from './form/edit_profile.js';
import { switchGameTab, openModal, searchFunction, addFriendHandler,
		 show_dynamic_history, show_dynamic_stats, show_dynamic_friends,
		friendsTab, deleteFriend } from './profile.js';
import { handleLogout } from './utils/logout.js';
import { changeAvatar } from './utils/avatar.js'; // a ajouter
import { message } from './utils/message.js';
import { dropdown } from './header.js';
import './notifs.js';
import { matchmacking } from './games/matchmaking.js';
import { pong3D } from './games/pong/pong.js';
import { ticTacToe3D } from './games/ticTacToe/ticTacToe.js';

window.addEventListener('hashchange', function() {
	let hash = window.location.hash.substring(1);
	let page = hash.split('?')[0];
	if (!page) {
		page = 'home';
	}
	showPage(page);
});

window.addEventListener('load', function() {
	let hash = window.location.hash.substring(1);
	let page = hash.split('?')[0];
	if (!page) {
		page = 'home';
	}
	window.searchFunction = searchFunction;
	showPage(page);
});

function is_logged_in()
{
	const is_logged_in = document.getElementById('logout-button');
	if (is_logged_in)
		return true;
	return false;
}

const pageHandlers = {
    'login': [handleLoginFormSubmit],
    'register': [handleRegisterFormSubmit, changeAvatar],
    'profile': [show_dynamic_friends, openModal, addFriendHandler, searchFunction,
				() => show_dynamic_history(1), () => show_dynamic_stats(1), friendsTab,
				switchGameTab, deleteFriend],
    'edit_profile': [handleEditProfileFormSubmit, changeAvatar],
    // 'game-1': [game, listenerGame],
    // 'game-2': [game, listenerGame]
};
async function executeHandlers(page) {
    for (const func of pageHandlers[page]) {
        await func();
    }
}

function showPage(page) {
	fetch(`/pages/${page}`)
	.then(response => response.json())
	.then(data => {
		const page_content = document.getElementById('page');
		if (!page_content) {
			console.error('Element with ID "page" not found');
			return ;
		}
		page_content.innerHTML = data.page;
		const isLogged = is_logged_in();
		if (!isLogged && page === 'home')
			handleLoginFormSubmit();
		else if (pageHandlers[page])
			executeHandlers(page);

		if (isLogged)
		{
			handleLogout();
			dropdown();
		}
	})
	.catch(error => {
		console.error(error);
	});
}
