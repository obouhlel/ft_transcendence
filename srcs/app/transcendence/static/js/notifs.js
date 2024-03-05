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
		let pageURL = window.location.hash.substring(1);
		if (pageURL == '')
			pageURL = 'home';
		const page = document.getElementById('page');
		console.log(pageURL);
		console.log(page);
		const data = await doRequest.get(`/pages/${pageURL}`);
		console.log(data.page);
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