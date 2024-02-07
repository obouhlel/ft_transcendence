// Assurez-vous que le DOM est complètement chargé avant d'ajouter des écouteurs d'événements

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = cookies[i].trim();
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {
	// Obtenez une référence au formulaire
	var form = document.getElementById('login-form');
	var csrftoken = getCookie('csrftoken');
	// Ajoutez un écouteur d'événements "submit" au formulaire
	form.addEventListener('submit', function(event) {
		// Empêchez le comportement par défaut du formulaire (qui est de recharger la page)
		event.preventDefault();

		// Obtenez les valeurs des champs de formulaire
		var username = document.getElementById('id_username').value;
		var password = document.getElementById('id_password').value;

		// Créez un objet avec les données du formulaire
		var data = {
			'username': username,
			'password': password
		};
		console.log("dataa: ", data); // A supprimer
		// Envoyez les données à votre serveur via une requête AJAX
		fetch('https://localhost:8000/login/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				// Incluez le token CSRF de Django dans les en-têtes de la requête
				'X-CSRFToken': csrftoken,
			},
			credentials: 'include',
			body: JSON.stringify(data)
		})
		.then(response => response.json())
		.then(data => {
			// Gérez la réponse de votre serveur ici
			console.log(data); // a supprimer
			var messageElement = document.getElementById('message');
			if (data.status === 'ok') {
				console.log('CONNEXION REUSSIEE');
				messageElement.textContent = data.message;
				messageElement.style.color = 'green';  // Changez la couleur du texte en vert
				// window.location.reload();
			} else if (data.status === 'error') {
				console.log('ERREUR DE CONNEXION');
				messageElement.textContent = data.message;
				messageElement.style.color = 'red';  // Changez la couleur du texte en rouge
			}
		})
		.catch(error => {
			// Gérez les erreurs ici
			var messageElement = document.getElementById('message');
			console.log('ERREUR DE CONNEXION');
			console.error(error);
			messageElement.textContent = 'Erreur de connexion';
			messageElement.style.color = 'red';
		});
	});
});


// logout
document.addEventListener('DOMContentLoaded', function() {
	var logoutButton = document.getElementById('logout-button');
	logoutButton.addEventListener('click', function(event) {
		event.preventDefault();
		fetch('https://localhost:8000/logout/', {
			method: 'GET',
			credentials: 'include'
		})
		.then(response => response.json())
		.then(data => {
			console.log(data);
			if (data.status === 'ok') {
				console.log('DECONNEXION REUSSIE');
				window.location.href = 'https://localhost:8000/'; // Redirigez l'utilisateur vers la page d'accueil
			} else if (data.status === 'error') {
				console.log('ERREUR DE DECONNEXION');
			}
		})
		.catch(error => {
			console.log('ERREUR DE DECONNEXION');
			console.error(error);
		});
	});
});
