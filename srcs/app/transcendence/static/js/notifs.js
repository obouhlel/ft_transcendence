export function handlerNotification() {
	// setup chat scoket
	const notifyScoket = new WebSocket(
		'wss://'
		+ window.location.host
		+ '/ws/notify/'
	);

	// on socket open
	notifyScoket.onopen = function (e) {
		console.log('Socket successfully connected.');
	};

	// on socket close
	notifyScoket.onclose = function (e) {
		console.log('Socket closed unexpectedly');
	};

	// on receiving message on group
	notifyScoket.onmessage = function (e) {
		const data = JSON.parse(e.data);
		const message = data.message;
		// Call the setMessage function to add the new li element
		setMessage(message);

	};

	function setMessage(message) {
		// Create a new li element
		const template = document.getElementById('notification');
		const newNotif = template.content.cloneNode(true);
		newNotif.querySelector('.message').textContent = message;
		document.getElementById('bellDropdown').appendChild(newNotif);
		let count = document.getElementById('bellDropdown').getAttribute('data-count');	
		count = parseInt(count) + 1;
		document.getElementById('bellDropdown').setAttribute('data-count', count);
		//document.getElementById('bellDropdown').classList.add('show');
	}

	// Listen for hash changes
	window.addEventListener('hashchange', function() {
		const pageNoNotification = ['login', 'register', '400', '401', '403', '404', '405'];
		const currentHash = window.location.hash.substring(1);
		if (pageNoNotification.includes(currentHash)) {
			notifyScoket.close();
		}
	});
}