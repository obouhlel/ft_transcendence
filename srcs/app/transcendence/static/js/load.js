import { handleLoginFormSubmit } from './form/login.js';
import { handleRegisterFormSubmit } from './form/register.js';
import { handleEditProfileFormSubmit } from './form/edit_profile.js';
import { switchGameTab, openModal, searchFunction, addFriendHandler,
		 show_dynamic_history, show_dynamic_stats, show_dynamic_friends,
		friendsTab, deleteFriend } from './profile.js';
import { handleLogout } from './utils/logout.js';
import { changeAvatar } from './utils/avatar.js';
import { message } from './utils/message.js';
import { dropdown } from './header.js';

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
    'register': [handleRegisterFormSubmit],
    'profile': [show_dynamic_friends, openModal, addFriendHandler, searchFunction,
				() => show_dynamic_history(1), () => show_dynamic_stats(1), friendsTab,
				switchGameTab, deleteFriend],
    'edit_profile': [handleEditProfileFormSubmit],
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
			return;
		}
		page_content.innerHTML = data.page;
		const isLogged = is_logged_in();
		if (!isLogged && page === 'home')
			handleLoginFormSubmit();
		else if (pageHandlers[page])
			executeHandlers(page);
		else
			console.error('Unknown page:', page);

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
