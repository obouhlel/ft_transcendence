import { doRequest } from './utils/fetch.js';
import { handleLogout } from './utils/logout.js';
import { dropdown, responsiveNav } from './header.js';

export async function handlerNotification() {
	// setup chat scoket
	const notifyScoket = new WebSocket(
		'wss://'
		+ window.location.host
		+ '/ws/notify/'
	);

	// on socket open
	notifyScoket.onopen = function (e) {
		console.log('Socket notify connected.');
	};

	// on socket close
	notifyScoket.onclose = function (e) {
		console.log('Socket notify closed unexpectedly');
	};

	// on receiving message on group
	notifyScoket.onmessage = function (e) {
		const data = JSON.parse(e.data);
		const message = data.message;
		setMessage(message);
	};

	async function setMessage(message) {
		const header = document.getElementById('header');
		const data = await doRequest.get(`/update_header/`);
		header.innerHTML = data.html;
		handleLogout();
		responsiveNav();
		dropdown();
	}

	// Listen for hash changes
	window.addEventListener('hashchange', function() {
		const pageNoNotification = ['login', 'register'];
		const currentHash = window.location.hash.substring(1);
		if (pageNoNotification.includes(currentHash)) {
			notifyScoket.close();
		}
	});
}