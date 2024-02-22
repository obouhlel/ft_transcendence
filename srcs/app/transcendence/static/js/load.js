import { handleLoginFormSubmit, handleLogoutFormSubmit } from './login.js';
import { handleRegisterFormSubmit } from './register.js';
import { handleEditProfileFormSubmit } from './profile.js';

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

function userIsLoggedIn() {
	if (document.cookie.includes('session_id')) {
		return true;
	}
	return false;
}

function showPage(page) {
    fetch(`/pages/${page}`)
    .then(response => response.json())
    .then(data => {
		const main = document.querySelector('main');
		const isLoggedIn = userIsLoggedIn();
		console.log('isLoggedIn:', isLoggedIn);
		console.log(main);
        main.innerHTML = data.page;
		if (page === 'home' && !isLoggedIn) {
			handleLoginFormSubmit();
		} else if (page === 'login') {
            handleLoginFormSubmit();
        } else if (page === 'register') {
            handleRegisterFormSubmit();
        }
        else if (page === 'edit_profile') {
            handleEditProfileFormSubmit();
        }
        handleLogoutFormSubmit();
    })
    .catch(error => {
        console.error(error);
    });
}