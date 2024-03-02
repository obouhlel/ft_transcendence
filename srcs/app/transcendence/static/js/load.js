import { handleLoginFormSubmit } from './form/login.js';
import { handleRegisterFormSubmit } from './form/register.js';
import { handleEditProfileFormSubmit } from './form/edit_profile.js';
import { handleLogout } from './utils/logout.js';
import { changeAvatar } from './utils/avatar.js';
import { message } from './utils/message.js';
import { gameTab, friendsTab } from './profile.js';
import { dropdown } from './header.js';
import { matchmacking } from './games/matchmaking.js';
import { pong3D } from './games/pong.js';
import { ticTacToe3D } from './games/ticTacToe.js';


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
	'400': message,
    'login': handleLoginFormSubmit,
    'register': () => {
		handleRegisterFormSubmit();
		changeAvatar();
	},
    'edit_profile': () => {
		handleEditProfileFormSubmit();
		changeAvatar();
	},
	'profile': () => {
        gameTab();
        friendsTab();
    },
    'game-1': () => {
		matchmacking('pong');
	},
	'game-2': () => {
		matchmacking('TicTacToe');
	},
	'pong': pong3D,
	'TicTacToe':  ticTacToe3D,
};

function showPage(page) {
	fetch(`/pages/${page}`)
	.then(response => response.json())
	.then(data => {
		console.log(data);
		console.log(page);
		const page_content = document.getElementById('page');
		page_content.innerHTML = data.page;
		const isLogged = is_logged_in();
		if (!isLogged && page === 'home')
			handleLoginFormSubmit();
		else if (pageHandlers[page])
			pageHandlers[page]();
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