/**
 * Main Application Logic for AirGuard AI Dashboard
 */

document.addEventListener('DOMContentLoaded', () => {
    // Initialize Lucide Icons
    lucide.createIcons();

    // DOM Elements
    const searchForm = document.getElementById('searchForm');
    const cityInput = document.getElementById('cityInput');
    const btnGeolocation = document.getElementById('btnGeolocation');
    const btnExportPDF = document.getElementById('btnExportPDF');
    const btnCopyJSON = document.getElementById('btnCopyJSON');
    const btnToggleChat = document.getElementById('btnToggleChat');
    const chatDrawer = document.getElementById('chatDrawer');
    const btnCloseChat = document.getElementById('btnCloseChat');
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatBody = document.getElementById('chatBody');
    const btnMultiCityModal = document.getElementById('btnMultiCityModal');
    const multiCityModal = document.getElementById('multiCityModal');
    const btnCloseModal = document.getElementById('btnCloseModal');
    const btnRunCompare = document.getElementById('btnRunCompare');
    const citiesCompareInput = document.getElementById('citiesCompareInput');
    const compareResultsContainer = document.getElementById('compareResultsContainer');

    let currentReport = null;

    // Load Default City on Startup
    loadAirQuality("Delhi");

    // Search Form Handler
    searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const city = cityInput.value.trim();
        if (city) {
            loadAirQuality(city);
        }
    });

    // Geolocation Handler
    btnGeolocation.addEventListener('click', () => {
        if (navigator.geolocation) {
            btnGeolocation.classList.add('pulse');
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    btnGeolocation.classList.remove('pulse');
                    loadAirQualityByCoords(pos.coords.latitude, pos.coords.longitude);
                },
                (err) => {
                    btnGeolocation.classList.remove('pulse');
                    alert("Geolocation failed or permission denied: " + err.message);
                }
            );
        } else {
            alert("Geolocation is not supported by your browser.");
        }
    });

    // Fetch Air Quality Data by City
    async function loadAirQuality(cityName) {
        try {
            showLoadingState();
            const res = await fetch(`/api/air-quality?city=${encodeURIComponent(cityName)}`);
            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.detail || "Failed to fetch air quality data");
            }
            const data = await res.json();
            currentReport = data;
            renderDashboard(data);
        } catch (err) {
            alert("Error: " + err.message);
        }
    }

    // Fetch Air Quality Data by Coords
    async function loadAirQualityByCoords(lat, lon) {
        try {
            showLoadingState();
            const res = await fetch(`/api/air-quality?lat=${lat}&lon=${lon}`);
            if (!res.ok) throw new Error("Failed to fetch air quality data");
            const data = await res.json();
            currentReport = data;
            renderDashboard(data);
        } catch (err) {
            alert("Error: " + err.message);
        }
    }

    function showLoadingState() {
        document.getElementById('aqiValue').innerText = "--";
        document.getElementById('riskLevelText').innerText = "Analyzing...";
        document.getElementById('riskReasonText').innerText = "Processing telemetry from Open-Meteo & uAgents AI...";
    }

    function renderDashboard(data) {
        const current = data.current_air_quality;
        const location = data.location;
        const risk = data.risk_assessment;
        const who = data.who_compliance;
        const health = data.health_advisory;
        const activities = data.activity_analyzer;
        const envIntel = data.environmental_intelligence;
        const green = data.green_sustainability;
        const alerts = data.emergency_alerts;

        // Location & AQI Card
        document.getElementById('locationBadge').innerHTML = `<i data-lucide="map-pin"></i> ${location.name}, ${location.country || ''}`;
        document.getElementById('aqiValue').innerText = current.aqi;
        document.getElementById('riskLevelText').innerText = risk.level + " Air Quality";
        document.getElementById('riskReasonText').innerText = risk.reason;

        // AQI Circle Color
        const circle = document.getElementById('aqiCircle');
        if (current.aqi <= 50) { circle.style.borderColor = "#10B981"; circle.style.boxShadow = "0 0 20px rgba(16, 185, 129, 0.4)"; }
        else if (current.aqi <= 100) { circle.style.borderColor = "#F59E0B"; circle.style.boxShadow = "0 0 20px rgba(245, 158, 11, 0.4)"; }
        else if (current.aqi <= 150) { circle.style.borderColor = "#F97316"; circle.style.boxShadow = "0 0 20px rgba(249, 115, 22, 0.4)"; }
        else { circle.style.borderColor = "#EF4444"; circle.style.boxShadow = "0 0 20px rgba(239, 68, 68, 0.4)"; }

        // Risk Score Bar
        document.getElementById('riskScoreVal').innerText = `${risk.score} / 100`;
        document.getElementById('riskScoreFill').style.width = `${risk.score}%`;

        // Dominant Pattern
        document.getElementById('dominantPatternText').innerText = data.pollution_patterns.dominant_pattern;

        // AI Scores Tile
        document.getElementById('scoreAir').innerText = green.scores.air_quality_score;
        document.getElementById('scoreHealth').innerText = green.scores.health_safety_score;
        document.getElementById('scoreEco').innerText = green.scores.environmental_score;
        document.getElementById('scoreSustain').innerText = green.scores.sustainability_score;

        // Trend Strip
        const trends = data.forecasting.trends;
        document.getElementById('trend1h').innerText = `${trends.next_hour.direction} (${trends.next_hour.expected_aqi})`;
        document.getElementById('trend24h').innerText = `${trends.tomorrow.direction} (${trends.tomorrow.expected_aqi})`;
        document.getElementById('trend7d').innerText = `${trends.next_7_days.direction} (${trends.next_7_days.expected_aqi})`;

        // Emergency Alerts Banner
        const banner = document.getElementById('emergencyBanner');
        if (alerts && alerts.length > 0) {
            banner.classList.remove('hidden');
            document.getElementById('emergencyTitle').innerText = alerts[0].type.toUpperCase();
            document.getElementById('emergencyDesc').innerText = `${alerts[0].message} ${alerts[0].recommendation}`;
        } else {
            banner.classList.add('hidden');
        }

        // Pollutant Matrix & WHO Badges
        const pollutantGrid = document.getElementById('pollutantGrid');
        pollutantGrid.innerHTML = '';
        Object.keys(who).forEach(key => {
            const p = who[key];
            const nameMap = {
                "pm2_5": "PM2.5", "pm10": "PM10", "nitrogen_dioxide": "NO₂",
                "sulphur_dioxide": "SO₂", "ozone": "O₃", "carbon_monoxide": "CO"
            };
            const pCard = document.createElement('div');
            pCard.className = 'pollutant-card';
            pCard.innerHTML = `
                <div class="pollutant-name">${nameMap[key] || key}</div>
                <div class="pollutant-val">${p.value} <small style="font-size:0.7rem;">${p.unit}</small></div>
                <span class="status-badge ${p.color_class}">${p.status}</span>
                <p style="font-size:0.7rem; color:var(--text-secondary); margin-top:0.3rem;">${p.description}</p>
            `;
            pollutantGrid.appendChild(pCard);
        });

        // Demographic Health List
        const demoList = document.getElementById('demographicList');
        demoList.innerHTML = '';
        const demographics = health.demographics;
        Object.keys(demographics).forEach(key => {
            const d = demographics[key];
            const formattedKey = key.replace(/_/g, ' ').toUpperCase();
            const dItem = document.createElement('div');
            dItem.className = 'demo-item';
            dItem.innerHTML = `
                <div class="demo-header">
                    <span class="demo-title"><i data-lucide="user"></i> ${formattedKey}</span>
                    <span class="status-badge ${d.risk_level.includes('High') || d.risk_level.includes('Severe') ? 'danger' : 'warning'}">${d.risk_level}</span>
                </div>
                <div class="demo-reason">${d.reason}</div>
                <div class="demo-rec">💡 ${d.recommendation}</div>
            `;
            demoList.appendChild(dItem);
        });

        // Activity Grid
        const activityGrid = document.getElementById('activityGrid');
        activityGrid.innerHTML = '';
        activities.forEach(act => {
            const aCard = document.createElement('div');
            aCard.className = 'act-card';
            aCard.innerHTML = `
                <div class="act-header">
                    <span class="act-title">${act.activity}</span>
                    <span class="act-score" style="color: ${act.suitability_score >= 70 ? '#10B981' : act.suitability_score >= 40 ? '#F59E0B' : '#EF4444'}">${act.suitability_score}</span>
                </div>
                <span class="status-badge ${act.risk_level === 'Low' ? 'success' : act.risk_level === 'Moderate' ? 'warning' : 'danger'}">${act.risk_level} Risk</span>
                <p class="act-rec" style="margin-top:0.3rem;">${act.recommendation}</p>
            `;
            activityGrid.appendChild(aCard);
        });

        // Environmental Intelligence
        const envIntelList = document.getElementById('envIntelList');
        envIntelList.innerHTML = '';
        Object.keys(envIntel).forEach(key => {
            const formatted = key.replace(/_/g, ' ').toUpperCase();
            const item = document.createElement('div');
            item.className = 'env-item';
            item.innerHTML = `
                <i data-lucide="globe" class="env-icon"></i>
                <div>
                    <strong style="color: var(--text-primary); font-size:0.8rem;">${formatted}</strong>
                    <p style="color: var(--text-secondary); font-size:0.78rem;">${envIntel[key]}</p>
                </div>
            `;
            envIntelList.appendChild(item);
        });

        // Carbon Box & Green Suggestions
        const carbon = green.carbon_footprint;
        document.getElementById('carbonValue').innerText = `${carbon.estimated_daily_co2_kg_per_capita} kg CO₂e / capita`;
        document.getElementById('carbonClass').innerText = `${carbon.severity_classification} in ${carbon.city}`;

        const greenList = document.getElementById('greenSuggestionsList');
        greenList.innerHTML = '';
        green.suggestions.forEach(s => {
            const gCard = document.createElement('div');
            gCard.className = 'green-card';
            gCard.innerHTML = `
                <h4>${s.title} (${s.category})</h4>
                <p>${s.impact}</p>
            `;
            greenList.appendChild(gCard);
        });

        // JSON Code Block
        document.getElementById('jsonPayloadBlock').innerText = JSON.stringify(data.multi_agent_payload, null, 2);

        // Render Chart.js
        renderSourceChart(data.pollution_sources);
        renderTrendChart(data.forecasting.hourly_raw || { us_aqi: data.current_air_quality.aqi ? [data.current_air_quality.aqi] : [] });
        renderBreakdownChart(current);

        lucide.createIcons();
    }

    // PDF Export
    btnExportPDF.addEventListener('click', () => {
        const element = document.getElementById('exportableArea');
        const opt = {
            margin:       0.3,
            filename:     `AirGuard_Report_${cityInput.value.trim() || 'City'}.pdf`,
            image:        { type: 'jpeg', quality: 0.98 },
            html2canvas:  { scale: 2, backgroundColor: '#0B0F19' },
            jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
        };
        html2pdf().set(opt).from(element).save();
    });

    // Copy JSON
    btnCopyJSON.addEventListener('click', () => {
        const jsonText = document.getElementById('jsonPayloadBlock').innerText;
        navigator.clipboard.writeText(jsonText);
        alert("uAgents JSON payload copied to clipboard!");
    });

    // Conversational AI Chat Drawer Toggle
    btnToggleChat.addEventListener('click', () => chatDrawer.classList.toggle('hidden'));
    btnCloseChat.addEventListener('click', () => chatDrawer.classList.add('hidden'));

    // Conversational Chat Form Submit
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = chatInput.value.trim();
        if (!query) return;

        // Append User Message
        const uMsg = document.createElement('div');
        uMsg.className = 'chat-msg user-msg';
        uMsg.innerText = query;
        chatBody.appendChild(uMsg);
        chatInput.value = '';
        chatBody.scrollTop = chatBody.scrollHeight;

        // Fetch AI Answer
        try {
            const res = await fetch('/api/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    query: query,
                    city: cityInput.value.trim() || "Delhi"
                })
            });
            const answerData = await res.json();

            const bMsg = document.createElement('div');
            bMsg.className = 'chat-msg bot-msg';
            bMsg.innerText = answerData.answer;
            chatBody.appendChild(bMsg);
            chatBody.scrollTop = chatBody.scrollHeight;
        } catch (err) {
            const bMsg = document.createElement('div');
            bMsg.className = 'chat-msg bot-msg';
            bMsg.innerText = "Sorry, I had trouble processing your query.";
            chatBody.appendChild(bMsg);
        }
    });

    // Multi-City Comparison Modal Handlers
    btnMultiCityModal.addEventListener('click', () => multiCityModal.classList.remove('hidden'));
    btnCloseModal.addEventListener('click', () => multiCityModal.classList.add('hidden'));

    btnRunCompare.addEventListener('click', async () => {
        const rawInput = citiesCompareInput.value.trim();
        if (!rawInput) return;
        const citiesList = rawInput.split(',').map(c => c.trim()).filter(c => c.length > 0);

        compareResultsContainer.innerHTML = '<p style="color:var(--accent-blue);">Running multi-city analysis...</p>';

        try {
            const res = await fetch('/api/compare', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ cities: citiesList })
            });
            const compData = await res.json();

            let html = `
                <div class="carbon-box">
                    <strong>Summary:</strong> ${compData.summary}
                </div>
                <table class="compare-table">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>City</th>
                            <th>AQI</th>
                            <th>PM2.5</th>
                            <th>Risk Level</th>
                            <th>Dominant Source</th>
                            <th>Health Score</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            compData.comparison.forEach((item, idx) => {
                html += `
                    <tr>
                        <td>#${idx + 1}</td>
                        <td><strong>${item.city}</strong></td>
                        <td><span class="status-badge ${item.aqi <= 50 ? 'success' : item.aqi <= 100 ? 'warning' : 'danger'}">${item.aqi}</span></td>
                        <td>${item.pm2_5} µg/m³</td>
                        <td>${item.risk_level}</td>
                        <td>${item.dominant_pattern}</td>
                        <td>${item.health_score} / 100</td>
                    </tr>
                `;
            });
            html += `</tbody></table>`;
            compareResultsContainer.innerHTML = html;
        } catch (err) {
            compareResultsContainer.innerHTML = `<p style="color:var(--accent-rose);">Failed to run comparison: ${err.message}</p>`;
        }
    });
});
