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
		var username = document.getElementById('username').value;
		var password = document.getElementById('password').value;

		// Créez un objet avec les données du formulaire
		var data = {
			'username': username,
			'password': password
		};
		// Envoyez les données à votre serveur via une requête AJAX
		fetch('http://localhost:8000/login/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				// Incluez le token CSRF de Django dans les en-têtes de la requête
				'X-CSRFToken': csrftoken,
			},
			credentials: 'include',
			body: JSON.stringify(data)
		})
		.then(response => {
			if (!response.ok) {
				throw new Error('Erreur HTTP, statut = ' + response.status);
			}
			return response.json();
		})
		.then(data => {
			// Gérez la réponse de votre serveur ici
			console.log(data);
			console.log('CONNEXION REUSSIE');
		})
		.catch(error => {
			// Gérez les erreurs ici
			console.log('ERREUR DE CONNEXION');
			console.error(error);
		});
	});
});
