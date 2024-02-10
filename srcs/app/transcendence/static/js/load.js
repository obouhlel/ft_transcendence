window.addEventListener('hashchange', function() {
    var section = window.location.hash.substring(1); // Supprime le '#'
    showSection(section);
});

function showSection(section) {
	fetch(`/sections/${section}`)
	.then(response => response.text())
	.then(data => {
		document.getElementById('section').innerHTML = data;


		// CA MARCHAIS PAS CAR IL FAUT RATTACHER LA GESTION DES EVENEMENTS AU DOM ICI vu que le DOM est modifié
		// BESOIN DE CLEAN LE CODE

		var form = document.getElementById('login-form');
        if (!form) { return; }
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            var username, password, data;

            username = document.getElementById('username').value;
            password = document.getElementById('password').value;
            data = {
                'username': username,
                'password': password
			};
            console.log('data:', data);
            // try {
            //     doRequest.Fetch(`${SERVER_URL}/login/`, 'POST', data, doRequest.callbackLogin);
            // } catch (error) {
            //     console.error('Une erreur est survenue lors de la connexion :', error);
            // }
        });


	})
	.catch(error => {
		console.error(error);
	});
}
