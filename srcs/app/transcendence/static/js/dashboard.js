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

