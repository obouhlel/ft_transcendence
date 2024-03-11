
function updateInfo(info, slider, name) {
	info.innerHTML = name + slider.value;
}

function pageGestion(sliderPoints, sliderPlayers, pointsInfo, playersInfo) {
	updateInfo(playersInfo, sliderPlayers, 'Players: ');
	updateInfo(pointsInfo, sliderPoints, 'Points: ');

	sliderPlayers.oninput = () => (updateInfo(playersInfo, sliderPlayers, 'Players: '));
	sliderPoints.oninput = () => (updateInfo(pointsInfo, sliderPoints, 'Points: '));
}

export function tournamentCreation(gameName) {
	const btn = document.getElementById('createTournament');
	const sliderPoints = document.getElementById('slider');
	const sliderPlayers = document.getElementById('slider2');
	const pointsInfo = document.getElementById('points');
	const playersInfo = document.getElementById('players');
	
	pageGestion(sliderPoints, sliderPlayers, pointsInfo, playersInfo);

	btn.addEventListener('click', () => {
		
	});
}