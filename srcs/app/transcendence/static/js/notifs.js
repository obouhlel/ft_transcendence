import { doRequest } from './utils/fetch.js';

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
		const games = ['pong', 'TicTacToe'];
		let pageURL = window.location.hash.substring(1);
		if (pageURL == '')
			pageURL = 'home';
		if (games.includes(pageURL))
			return (setMessage(message));
		const page = document.getElementById('page');
		const data = await doRequest.get(`/pages/${pageURL}`);
		page.innerHTML = data.page;
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