/**
 * Chart.js Manager for AirGuard AI Dashboard
 */

let sourceChartInstance = null;
let trendChartInstance = null;
let breakdownChartInstance = null;

function renderSourceChart(sources) {
    const ctx = document.getElementById('sourceChart');
    if (!ctx) return;

    if (sourceChartInstance) {
        sourceChartInstance.destroy();
    }

    const labels = sources.slice(0, 5).map(s => s.source);
    const data = sources.slice(0, 5).map(s => s.confidence);

    sourceChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    '#EF4444',
                    '#F59E0B',
                    '#8B5CF6',
                    '#3B82F6',
                    '#10B981'
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: { color: '#9CA3AF', font: { size: 10 } }
                }
            },
            cutout: '70%'
        }
    });
}

function renderTrendChart(hourlyData) {
    const ctx = document.getElementById('trendChart');
    if (!ctx) return;

    if (trendChartInstance) {
        trendChartInstance.destroy();
    }

    const timeLabels = (hourlyData.time || []).slice(0, 48).map(t => {
        const d = new Date(t);
        return `${d.getHours()}:00`;
    });
    const aqiSeries = (hourlyData.us_aqi || []).slice(0, 48);

    trendChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: timeLabels,
            datasets: [{
                label: 'US AQI Trend (Next 48 Hours)',
                data: aqiSeries,
                borderColor: '#3B82F6',
                backgroundColor: 'rgba(59, 130, 246, 0.15)',
                fill: true,
                tension: 0.4,
                pointRadius: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { ticks: { color: '#9CA3AF', maxTicksLimit: 12 }, grid: { display: false } },
                y: { ticks: { color: '#9CA3AF' }, grid: { color: 'rgba(255, 255, 255, 0.05)' } }
            },
            plugins: {
                legend: { labels: { color: '#F3F4F6' } }
            }
        }
    });
}

function renderBreakdownChart(current) {
    const ctx = document.getElementById('breakdownChart');
    if (!ctx) return;

    if (breakdownChartInstance) {
        breakdownChartInstance.destroy();
    }

    const pollutants = ['PM2.5', 'PM10', 'NO2', 'SO2', 'O3'];
    const values = [
        current.pm2_5 || 0,
        current.pm10 || 0,
        current.no2 || 0,
        current.so2 || 0,
        current.o3 || 0
    ];

    breakdownChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: pollutants,
            datasets: [{
                label: 'Concentration (µg/m³)',
                data: values,
                backgroundColor: [
                    '#EF4444',
                    '#F59E0B',
                    '#3B82F6',
                    '#8B5CF6',
                    '#10B981'
                ],
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { ticks: { color: '#9CA3AF' }, grid: { display: false } },
                y: { ticks: { color: '#9CA3AF' }, grid: { color: 'rgba(255, 255, 255, 0.05)' } }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}
