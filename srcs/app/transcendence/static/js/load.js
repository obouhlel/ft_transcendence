import { handleLoginFormSubmit, handleLogoutFormSubmit } from './login.js';
import { handleRegisterFormSubmit } from './register.js';

window.addEventListener('hashchange', function() {
	const page = window.location.hash.substring(1);
	showPage(page);
});

window.addEventListener('load', function() {
	let page = window.location.hash.substring(1);
	if (!page) {
		page = 'home';
	}
	showPage(page);
});

// const pages = {

// }

function showPage(page) {
	fetch(`/pages/${page}`)
	.then(response => response.json())
	.then(data => {
		const main = document.querySelector('main');
		console.log('Page :', page);
		console.log('JSON :', data);
		main.innerHTML = data.page;
		console.log(main);
		if (page === 'login') {
			handleLoginFormSubmit();
		} else if (page === 'register') {
			handleRegisterFormSubmit();
		} else if (page === 'logout') {
			handleLogoutFormSubmit();
		}
	})
	.catch(error => {
		console.error(error);
	});
}
