export async function fetchUserDataAndRenderChart() {
    const url = '/api/get_all_users/';
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error('Network response was not ok');
      
      const data = await response.json();
      if (data.status !== 'ok' || !Array.isArray(data.users)) throw new Error('Unexpected data format');
      
      const demographics = data.users.reduce((acc, user) => {
        const sex = user.sexe || 'O';
        acc[sex] = (acc[sex] || 0) + 1;
        return acc;
      }, {});
  
      renderChart(demographics);
    } catch (error) {
      // console.error('Error fetching user data:', error);
    }
  }

  function renderChart(demographics) {
  const ctx = document.getElementById('genderDemographicsChart').getContext('2d');
  const chart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Female', 'Male', 'Other'],
      datasets: [{
        label: 'Sex Demographics',
        data: [demographics['F'], demographics['M'], demographics['N']],
        backgroundColor: [
          'rgba(255, 99, 132)',
          'rgba(54, 162, 235)', 
          'rgba(255, 206, 86)'  
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: false,
      plugins: {
        legend: {
          position: 'top',
          labels: {
            color: 'white',
          }
        },
        title: {
          display: false,
          text: 'User Sex Demographics'
        }
      }
    }
  });
}


export async function fetchUserDataAndProcessAges() {
  const url = '/api/get_all_users/';
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error('Network response was not ok');
    
    const data = await response.json();
    if (data.status !== 'ok' || !Array.isArray(data.users)) throw new Error('Unexpected data format');
    
    const ageRanges = {
      '18-24': 0,
      '25-34': 0,
      '35-44': 0,
      '45+': 0
    };
    
    data.users.forEach(user => {
      const age = calculateAge(new Date(user.birthdate));
      if (age >= 18 && age <= 24) ageRanges['18-24']++;
      else if (age >= 25 && age <= 34) ageRanges['25-34']++;
      else if (age >= 35 && age <= 44) ageRanges['35-44']++;
      else if (age >= 45) ageRanges['45+']++;
    });

    renderAgeDemographicsChart(ageRanges);
  } catch (error) {
    console.error('Error fetching user data:', error);
  }
}

function calculateAge(birthdate) {
  const today = new Date();
  let age = today.getFullYear() - birthdate.getFullYear();
  const m = today.getMonth() - birthdate.getMonth();
  if (m < 0 || (m === 0 && today.getDate() < birthdate.getDate())) {
    age--;
  }
  return age;
}


function renderAgeDemographicsChart(ageRanges) {
  const ctx = document.getElementById('ageDemographicsChart').getContext('2d');
  const chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: Object.keys(ageRanges),
      datasets: [{
        data: Object.values(ageRanges),
        backgroundColor: [
          'rgba(255, 99, 132)',
          'rgba(54, 162, 235)',
          'rgba(255, 206, 86)',
          'rgba(75, 192, 192)'
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        x: {
          ticks: {
            color: '#FFF', 
          },
          title: {
            display: true,
            text: 'Age Range',
            color: '#FFF'
          }
        },
        y: {
          ticks: {
            color: '#FFF',
          },
          title: {
            display: true,
            text: 'Number of Users',
            color: '#FFF' 
          }
        }
      },
      plugins: {
        legend: {
          display: false 
        }
      }
    }
  });
}

async function fetchLeaderboardData(gameId) {
  const leaderboardUrl = `/api/get_leaderboard/${gameId}`;
  const usersUrl = '/api/get_all_users/';

  try {
    const [leaderboardResponse, usersResponse] = await Promise.all([
      fetch(leaderboardUrl).then(res => res.json()),
      fetch(usersUrl).then(res => res.json()),
    ]);

    return {
      leaderboardData: leaderboardResponse,
      usersData: usersResponse,
    };
  } catch (error) {
    console.error("Error fetching data:", error);
    return { leaderboardData: null, usersData: null };
  }
}

function processAndAssociateData(leaderboardData) {
  const leaderboard = leaderboardData.users.map(entry => {
    const { user, stat } = entry;
    let ratio = 0;
    if (stat.nb_win + stat.nb_lose > 0) {
        ratio = (stat.nb_win / (stat.nb_win + stat.nb_lose)) * 100;
    }

    return {
        username: user.username,
        avatar: user.avatar || defaultAvatarUrl,
        nbPlayed: stat.nb_played,
        ratio: ratio,
        nb_win: stat.nb_win,
        nb_lose: stat.nb_lose,
    };
  });

  // Sort by ratio, descending
  leaderboard.sort((a, b) => b.ratio - a.ratio);

  // Assign ranks, taking ties into account
  let lastRatio = null;
  let lastRank = 0;
  let tiesCount = 0;

  leaderboard.forEach((item, index) => {
    if (item.ratio === lastRatio) {
      item.rank = lastRank;
      tiesCount++;
    } else {
      lastRank += 1 + tiesCount;
      item.rank = lastRank;
      lastRatio = item.ratio;
      tiesCount = 0;
    }
  });

  return leaderboard;
}



function displayLeaderboard(leaderboard) {
  const tbody = document.getElementById('leaderboardBody');
  tbody.innerHTML = '';

  leaderboard.forEach(entry => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
          <td>${entry.rank}</td>
          <td class="lead-user-td">
              <img src="${entry.avatar}" class="img-leaderboard" alt="user">&nbsp;
              <span class="name-leaderboard">${entry.username}</span>
          </td>
          <td>${entry.nbPlayed}</td>
          <td>${entry.ratio.toFixed(2)}%</td>
      `;
      tbody.appendChild(tr);
  });
}


async function fetchCurrentUserName() {
  const response = await fetch('/api/get_user_name/');
  const data = await response.json();
  return data.username;
}

async function updateDashboardStats(leaderboard) {
  const currentUser = await fetchCurrentUserName();
  const currentUserEntry = leaderboard.find(player => player.username === currentUser);
  const currentUserRank = currentUserEntry ? currentUserEntry.rank : 'N/A';

  const bestPlayer = leaderboard.length > 0 ? leaderboard[0] : null;
  const totalPlayers = leaderboard.length;

  document.querySelector('.dashboard-card h1').innerText = `#${currentUserRank}`;
  document.querySelector('.best-player-name').innerText = bestPlayer ? bestPlayer.username : 'N/A';
  document.querySelector('.best-player img').src = bestPlayer && bestPlayer.avatar ? bestPlayer.avatar : defaultAvatarUrl; // Ensure defaultAvatarUrl is correctly defined
  document.querySelectorAll('.dashboard-card')[2].querySelector('h1').innerText = totalPlayers.toString();
}

async function updateWinLossChart(leaderboard) {
  const currentUser = await fetchCurrentUserName();
  const currentUserData = leaderboard.find(entry => entry.username === currentUser);
  const messageElement = document.getElementById('chartMessage');
  const chartElement = document.getElementById('winLossChart');
  
  let totalWins = 0;
  let totalLosses = 0;

  if (currentUserData && currentUserData.nbPlayed > 0) {
      totalWins = currentUserData.nb_win;
      totalLosses = currentUserData.nb_lose;
      
      messageElement.style.display = 'none';
      chartElement.style.display = 'block';

  
      if (window.winLossChartInstance) {
          window.winLossChartInstance.destroy();
      }

      window.winLossChartInstance = new Chart(chartElement.getContext('2d'), {
          type: 'doughnut',
          data: {
              labels: ['Wins', 'Losses'],
              datasets: [{
                  data: [totalWins, totalLosses],
                  backgroundColor: [
                      'rgba(75, 192, 192, 1)',
                      'rgba(255, 99, 132, 1)'
                  ],
                  borderColor: [
                      'rgba(75, 192, 192, 1)',
                      'rgba(255, 99, 132, 1)'
                  ],
                  borderWidth: 1
              }]
          },
          options: {
              responsive: true,
              plugins: {
                  legend: {
                      position: 'top',
                      labels: {
                        color: 'white',
                      }
                  }
              }
          }
      });
  } else {

      messageElement.textContent = 'You have not played any games yet.';
      messageElement.style.display = 'block';
      chartElement.style.display = 'none';
  }
}


export async function updateDashboardDisplay(gameId) {
  const { leaderboardData, usersData } = await fetchLeaderboardData(gameId);
  if (leaderboardData.status === "ok" && usersData.status === "ok") {
      const leaderboard = processAndAssociateData(leaderboardData);
      displayLeaderboard(leaderboard);
      updateDashboardStats(leaderboard);
      updateWinLossChart(leaderboard);
  } else {
      console.error("Failed to fetch data");
  }
}

export function setupTabEventListeners() {
  document.querySelectorAll('.tab-link').forEach(tab => {
    tab.addEventListener('click', function() {
      document.querySelectorAll('.tab-link').forEach(t => t.classList.remove('active'));
      this.classList.add('active');

      const gameId = this.getAttribute('data-tab') === 'tab1' ? 1 : 2;
      updateDashboardDisplay(gameId);
    });
  });
}

