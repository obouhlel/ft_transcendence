import { pageHandlers } from './pages.js';
import { handleLoginFormSubmit } from './form/login.js';
import { handleLogout } from './utils/logout.js';
import { dropdown, responsiveNav } from './header.js';
import { searchFunction } from './profile.js';
import { handlerNotification } from './notifs.js';

let isNotificationHandled = false;

window.addEventListener('hashchange', function() {
	let page = hashChangeHandler();
	window.searchFunction = searchFunction;
	showPage(page);
});

window.addEventListener('load', function() {
	let page = hashChangeHandler();
	window.searchFunction = searchFunction;
	showPage(page);
});

function hashChangeHandler() {
	let hash = window.location.hash.substring(1);
	let page = hash.split('?')[0];
	if (!page) {
		page = 'home';
	}
	return page;
}

function is_logged_in()
{
	const is_logged_in = document.getElementById('logout-button');
	if (is_logged_in)
		return true;
	return false;
}

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
			responsiveNav();
			dropdown();
			if (!isNotificationHandled)
			{
				handlerNotification();
				isNotificationHandled = true;
			}
		}
		if (!isLogged)
			isNotificationHandled = false;
	})
	.catch(error => {
		console.error(error);
	});
}