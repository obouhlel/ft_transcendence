export function openVersusModal()
{
	const versusModal = document.querySelector('.versus-modal');
	const overlay = document.querySelector('.overlay');

	if (!versusModal || !overlay)
	{
		console.error('Element not found');
		return ;
	}

	versusModal.classList.remove('display-hidden');
	overlay.classList.remove('display-hidden');

	// Hide the modal after 5 seconds
	setTimeout(() => {
		versusModal.classList.add('display-hidden');
		overlay.classList.add('display-hidden');
	}, 3000);

}

export function openWinnerModal(winnerName) {
	const winnerModal = document.querySelector('.winner-modal');
	const overlay = document.querySelector('.overlay');

	if (!winnerModal || !overlay) {
		console.error('Element not found');
		return;
	}

	fetch(`/api/get_user_by_username/${winnerName}`)
		.then(response => response.json())
		.then(data => {
			const winnerImg = winnerModal.querySelector('.winner-avatar');

			if (!winnerImg) {
				console.error('Element not found');
				return ;
			}

			console.log(data);
			
			if (data.user.avatar) winnerImg.src = data.user.avatar;
		});
	
	const winnerElement = document.getElementById('winner');
	if (!winnerElement) {
		console.error('Element not found');
		return ;
	}
	console.log(winnerName);
	console.log(winnerElement);
	winnerElement.textContent = winnerName;

	winnerModal.classList.remove('winner-hidden');
	overlay.classList.remove('display-hidden');

	setTimeout(() => {
		winnerModal.classList.add('winner-hidden');
		overlay.classList.add('display-hidden');
	}, 3000);
}