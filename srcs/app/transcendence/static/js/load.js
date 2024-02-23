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

const pageHandlers = {
    'home': handleLoginFormSubmit,
    'login': handleLoginFormSubmit,
    'register': handleRegisterFormSubmit,
    'edit_profile': handleEditProfileFormSubmit,
    'game': () => {
        game();
        listenerGame();
    }
};

function showPage(page) {
	fetch(`/pages/${page}`)
	.then(response => response.json())
	.then(data => {
		const page_content = document.getElementById('page');
		console.log('page :', page);
		console.log('data :', data);
		console.log('pageHandlers :', pageHandlers[page]);
		console.log(page_content);
		page_content.innerHTML = data.page;
		if (pageHandlers[page]) 
			pageHandlers[page]();
		handleLogoutFormSubmit();
	})
	.catch(error => {
		console.error(error);
	});
}