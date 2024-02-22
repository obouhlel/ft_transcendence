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

function showPage(page) {
    fetch(`/pages/${page}`)
    .then(response => response.json())
    .then(data => {
		const page_content = document.getElementById('page');
		console.log('page :', page);
        console.log('data :', data);
		console.log(page_content);
        page_content.innerHTML = data.page;
		if (page === 'home')
        {
			handleLoginFormSubmit();
		}
        else if (page === 'login')
        {
            handleLoginFormSubmit();
        }
        else if (page === 'register')
        {
            handleRegisterFormSubmit();
        }
        else if (page === 'edit_profile')
        {
            handleEditProfileFormSubmit();
        }
        else if (page === 'game')
        {
            game();
            listenerGame();
        }
        handleLogoutFormSubmit();
    })
    .catch(error => {
        console.error(error);
    });
}