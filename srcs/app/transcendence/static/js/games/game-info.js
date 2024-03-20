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
	}, 5000);

}

export function openWinnerModal() {
	const winnerModal = document.querySelector('.winner-modal');
	const overlay = document.querySelector('.overlay');

	if (!winnerModal || !overlay) {
		console.error('Element not found');
		return;
	}

	winnerModal.classList.remove('winner-hidden');
	overlay.classList.remove('display-hidden');

	// Hide the modal after 5 seconds
	setTimeout(() => {
		winnerModal.classList.add('winner-hidden');
		overlay.classList.add('display-hidden');
	}, 5000);
}