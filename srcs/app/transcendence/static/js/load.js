import { handleLoginFormSubmit, handleLogoutFormSubmit } from './login.js';
import { handleRegisterFormSubmit } from './register.js';

window.addEventListener('hashchange', function() {
    const section = window.location.hash.substring(1); // Supprime le '#'
    showSection(section);
});

window.addEventListener('load', function() {
    let section = window.location.hash.substring(1);
    if (!section) {
        section = 'home';
    }
    showSection(section);
});

function showSection(section) {
    fetch(`/sections/${section}`)
    .then(response => response.text())
    .then(data => {
		if (section != 'logout')
        	document.getElementById('section').innerHTML = data;
		console.log('section:', section);
        if (section === 'login') {
            handleLoginFormSubmit();
        } else if (section === 'register') {
            handleRegisterFormSubmit();
        } else if (section === 'logout') {
			handleLogoutFormSubmit();
        } else if (section === 'games') {
            getGames();
        }
    })
    .catch(error => {
        console.error(error);
    });
}
