import { handleLoginFormSubmit, handleLogoutFormSubmit } from './login.js';
import { handleRegisterFormSubmit } from './register.js';

window.addEventListener('hashchange', function() {
    const page = window.location.hash.substring(1); // Supprime le '#'
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
        console.log('data:', data);
		console.log('page:', page);
        document.getElementById('page').innerHTML = data.page;
        if (page === 'login') {
            handleLoginFormSubmit();
        } else if (page === 'register') {
            handleRegisterFormSubmit();
        } else if (section === 'logout') {
			handleLogoutFormSubmit();
		}
    })
    .catch(error => {
        console.error(error);
    });
}
