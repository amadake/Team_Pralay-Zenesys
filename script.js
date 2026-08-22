// DEMAND FORECAST CHART
const demandCtx = document.getElementById('demandChart').getContext('2d');
new Chart(demandCtx, {
    type: 'line',
    data: {
        labels: ['Aug 18', 'Aug 19', 'Aug 20', 'Aug 21', 'Aug 22', 'Aug 23', 'Aug 24'],
        datasets: [{
            label: 'Actual Sales',
            data: [200, 350, 300, 420, 580, null, null],
            borderColor: '#3b82f6',
            backgroundColor: (context) => {
                const gradient = demandCtx.createLinearGradient(0, 0, 0, 300);
                gradient.addColorStop(0, 'rgba(59, 130, 246, 0.2)');
                gradient.addColorStop(1, 'rgba(59, 130, 246, 0)');
                return gradient;
            },
            fill: true,
            tension: 0.4,
            pointRadius: 4,
            pointBackgroundColor: '#3b82f6'
        }, {
            label: 'Forecast',
            data: [null, null, null, null, 580, 750, 950],
            borderColor: '#8b5cf6',
            borderDash: [5, 5],
            fill: false,
            tension: 0.4,
            pointRadius: 0
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
            y: {
                beginAtZero: true,
                grid: { color: '#f1f5f9' },
                ticks: { font: { size: 10 }, color: '#94a3b8' }
            },
            x: {
                grid: { display: false },
                ticks: { font: { size: 10 }, color: '#94a3b8' }
            }
        }
    }
});

// INVENTORY HEALTH CHART
const healthCtx = document.getElementById('healthChart').getContext('2d');
new Chart(healthCtx, {
    type: 'doughnut',
    data: {
        labels: ['Healthy', 'Low', 'Out'],
        datasets: [{
            data: [86, 8, 6],
            backgroundColor: ['#22c55e', '#f59e0b', '#ef4444'],
            borderWidth: 0,
            hoverOffset: 4
        }]
    },
    options: {
        cutout: '80%',
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } }
    }
});