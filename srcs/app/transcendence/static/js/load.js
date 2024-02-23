import { handleLoginFormSubmit, handleLogoutFormSubmit } from './login.js';
import { handleRegisterFormSubmit } from './register.js';
import { handleEditProfileFormSubmit } from './profile.js';
import { game, listenerGame } from './game.js';

window.addEventListener('hashchange', function() {
	let page = window.location.hash.substring(1);
	if (!page) {
		page = 'home';
	}
	showPage(page);
});

window.addEventListener('load', function() {
	let page = window.location.hash.substring(1);
	if (!page) {
		page = 'home';
	}
	showPage(page);
});

function is_logged_in()
{
	const is_logged_in = document.getElementById('logged');
	if (is_logged_in)
		return true;
	return false;
}

const pageHandlers = {
    'login': handleLoginFormSubmit,
    'register': handleRegisterFormSubmit,
    'edit_profile': handleEditProfileFormSubmit,
    'game-1': () => {
        game();
        listenerGame();
    },
	'game-2': () => {
        game();
        listenerGame();
    }
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
			handleLogoutFormSubmit();
	})
	.catch(error => {
		console.error(error);
	});
}