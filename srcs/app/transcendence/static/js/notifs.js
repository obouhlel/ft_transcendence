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
		console.log(data);
		updateHeader();
	};

	// Listen for hash changes
	window.addEventListener('hashchange', function() {
		const pageNoNotification = ['login', 'register'];
		const currentHash = window.location.hash.substring(1);
		if (pageNoNotification.includes(currentHash)) {
			notifyScoket.close();
		}
	});
}

async function updateHeader() {
	const header = document.getElementById('header');
	const data = await doRequest.get(`/update_header/`);
	header.innerHTML = data.html;
	handleNotificationVisual();
	handleLogout();
	responsiveNav();
	dropdown();
}

export function handleNotificationVisual() {
	let count = document.querySelectorAll('.notif').length;
	if (count > 0)
	{
		const bellBtn = document.querySelector('.bell-btn');
		bellBtn.classList.add('show-notification');
	}
	else
	{
		const bellBtn = document.querySelector('.bell-btn');
		bellBtn.classList.remove('show-notification');
	}
}

export function handlerNotificationAction() {
	const acceptButtons = document.querySelectorAll('.accept-request');
	const denyButtons = document.querySelectorAll('.deny-request');
	const notificationIds = [];
	acceptButtons.forEach(button => {
		const notificationId = button.id.split('-')[1];
		notificationIds.push(notificationId);
	});
	denyButtons.forEach(button => {
		const notificationId = button.id.split('-')[1];
		notificationIds.push(notificationId);
	});
	acceptButtons.forEach(button => {
		button.addEventListener('click', async function() {
			handleNotificationVisual();
		});
	});
	denyButtons.forEach(button => {
		button.addEventListener('click', async function() {
			handleNotificationVisual();
		});
	});
}