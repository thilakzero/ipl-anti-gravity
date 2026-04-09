// Data Models
const cskColor = '#fbbc05'; // Yellow
const rcbColor = '#ea4335'; // Red
const neutralColor = '#00d2ff'; // Cyan for neutral/highlighted elements

// 1. Win Probability Donut Chart
const winCtx = document.getElementById('winChart').getContext('2d');
new Chart(winCtx, {
    type: 'doughnut',
    data: {
        labels: ['CSK (Team A) Win %', 'RCB (Team B) Win %'],
        datasets: [{
            data: [48.5, 51.5],
            backgroundColor: [cskColor, rcbColor],
            borderWidth: 0,
            hoverOffset: 8
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { position: 'bottom', labels: { color: '#e0e6ed', font: { family: 'Outfit', size: 14 } } }
        },
        cutout: '75%'
    }
});

// 2. Gravity Index Bar Chart
const indexCtx = document.getElementById('indexChart').getContext('2d');
new Chart(indexCtx, {
    type: 'bar',
    data: {
        labels: ['Team A (CSK)', 'Team B (RCB)'],
        datasets: [
            {
                label: 'Base Gravity',
                data: [865, 852],
                backgroundColor: 'rgba(139, 155, 180, 0.3)',
                borderColor: 'rgba(139, 155, 180, 1)',
                borderWidth: 1,
            },
            {
                label: 'Adjusted Gravity (+Pitch/Dew)',
                data: [845, 907], // CSK base reduced due to dew, RCB increased
                backgroundColor: [cskColor, rcbColor],
                borderWidth: 0,
                borderRadius: 4
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: { beginAtZero: false, min: 800, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#8b9bb4', font: { family: 'Outfit' } } },
            x: { grid: { display: false }, ticks: { color: '#e0e6ed', font: { family: 'Outfit', weight: 'bold', size: 14 } } }
        },
        plugins: {
            legend: { labels: { color: '#e0e6ed', font: { family: 'Outfit' } } }
        }
    }
});

// 3. Player Matchup Radar Chart
const radarCtx = document.getElementById('radarChart').getContext('2d');
new Chart(radarCtx, {
    type: 'radar',
    data: {
        labels: [
            'Form (Recent)', 
            'Strike/Economy Rate', 
            'Anti-Gravity Resistance', 
            'Venue Multiplier', 
            'Pressure Handling'
        ],
        datasets: [
            {
                label: 'Ruturaj Gaikwad (CSK)',
                data: [88, 85, 70, 75, 80],
                backgroundColor: 'rgba(251, 188, 5, 0.2)',
                borderColor: cskColor,
                pointBackgroundColor: cskColor,
                borderWidth: 2
            },
            {
                label: 'Virat Kohli (RCB)',
                data: [95, 80, 90, 100, 95],
                backgroundColor: 'rgba(234, 67, 53, 0.2)',
                borderColor: rcbColor,
                pointBackgroundColor: rcbColor,
                borderWidth: 2
            },
            {
                label: 'Shivam Dube (CSK)',
                data: [92, 98, 88, 80, 85],
                backgroundColor: 'rgba(0, 210, 255, 0.2)',
                borderColor: neutralColor,
                pointBackgroundColor: neutralColor,
                borderWidth: 2,
                borderDash: [5, 5]
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            r: {
                angleLines: { color: 'rgba(255,255,255,0.1)' },
                grid: { color: 'rgba(255,255,255,0.1)' },
                pointLabels: { color: '#e0e6ed', font: { family: 'Outfit', size: 13, weight: 'bold' } },
                ticks: { display: false, min: 0, max: 100 }
            }
        },
        plugins: {
            legend: { position: 'right', labels: { color: '#e0e6ed', font: { family: 'Outfit' } } }
        }
    }
});
