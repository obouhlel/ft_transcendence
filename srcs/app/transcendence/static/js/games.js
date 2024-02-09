import { SERVER_URL, doRequest } from './fetch.js';

document.addEventListener('DOMContentLoaded', function() {
	var btn = document.getElementById('test-btn');
	if (!btn) { return; }
	btn.addEventListener('click', function(event) {
		event.preventDefault();

		doRequest.Fetch(`${SERVER_URL}/games/`, 'GET', null, console.log);
	});
});


