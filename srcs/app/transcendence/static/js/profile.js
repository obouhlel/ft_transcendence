import { SERVER_URL, doRequest } from './fetch.js';

export function handleEditProfileFormSubmit() {
	const form = document.getElementById('profile-form');
	if (!form) { return; }
	form.addEventListener('submit', function(event) {
		event.preventDefault();

		const fields = ['username', 'firstname', 'lastname', 'email', 'password', 'password_confirm', 'avatar', 'birthdate', 'sexe'];

		let data = new FormData();
		fields.forEach(field => {
			let element = document.getElementById(field);
			if (element) {
				let value = field === 'avatar' ? element.files[0] : element.value;
				data.append(field, value);
			} else {
				console.log(`Element with ID ${field} not found`);
			}
		});

		console.log("data edit: ", Object.fromEntries(data.entries()));

		doRequest.Fetch(`${SERVER_URL}/api/edit_profile/`, 'POST', data, doRequest.callbackProfile);
	});
};

/*ACTIVE GAME-TAB FUNCTIONALITY IN USER PROFILE*/
export function gameTab()
{
	document.querySelectorAll('.tab-link').forEach(function(link) {
		link.addEventListener('click', function(e) {
			e.preventDefault(); // Prevent default anchor behavior

			// Get the tab ID from data-tab attribute
			const tabId = this.getAttribute('data-tab');

			// Remove active class from all tab links
			document.querySelectorAll('.tab-link').forEach(function(link) {
				link.classList.remove('active');
			});

			// Add active class to the current tab link
			this.classList.add('active');

			// Hide all tab contents
			document.querySelectorAll('.tab-content').forEach(function(tab) {
				tab.classList.remove('active-tab');
			});

			// Show the current tab content
			document.getElementById(tabId).classList.add('active-tab');
		});
	});
}
