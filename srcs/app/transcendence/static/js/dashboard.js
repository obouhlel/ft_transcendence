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
      console.error('Error fetching user data:', error);
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

async function fetchLeaderboardData() {
  const leaderboardUrl = '/api/get_leaderboard/1';
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

      return {
          username: user.username,
          avatar: user.avatar || defaultAvatarUrl,
          nbPlayed: stat.nb_played,
          ratio: stat.ratio * 100,
      };
  });

  // Sort by ratio, descending
  leaderboard.sort((a, b) => b.ratio - a.ratio);

  return leaderboard;
}

function displayLeaderboard(leaderboard) {
  const tbody = document.getElementById('leaderboardBody');
  tbody.innerHTML = '';

  leaderboard.forEach((entry, index) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${index + 1}</td>
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
  const currentUserIndex = leaderboard.findIndex(player => player.username === currentUser);
  const currentUserRank = currentUserIndex !== -1 ? currentUserIndex + 1 : 'N/A';

  const bestPlayer = leaderboard.length > 0 ? leaderboard[0] : null;
  const totalPlayers = leaderboard.length; 

  document.querySelector('.dashboard-card h1').innerText = `#${currentUserRank}`;
  document.querySelector('.best-player-name').innerText = bestPlayer ? bestPlayer.username : 'N/A';
  document.querySelector('.best-player img').src = bestPlayer && bestPlayer.avatar ? bestPlayer.avatar : defaultAvatarUrl; // Fallback to default avatar
  document.querySelectorAll('.dashboard-card')[2].querySelector('h1').innerText = totalPlayers;
}

export async function updateDashboardDisplay() {
  const { leaderboardData, usersData } = await fetchLeaderboardData();
  if (leaderboardData.status === "ok" && usersData.status === "ok") {
      const leaderboard = processAndAssociateData(leaderboardData);
      displayLeaderboard(leaderboard);
      updateDashboardStats(leaderboard);
  } else {
      console.error("Failed to fetch data");
  }
}