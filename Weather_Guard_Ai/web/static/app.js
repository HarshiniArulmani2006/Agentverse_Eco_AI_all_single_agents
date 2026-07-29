/**
 * WeatherWise AI - Dashboard Frontend Interactivity Script
 */

document.addEventListener("DOMContentLoaded", () => {
    fetchWeatherData("Coimbatore");
    
    // Support enter key on city input & chat input
    document.getElementById("cityInput").addEventListener("keypress", (e) => {
        if (e.key === "Enter") fetchWeatherData();
    });
    document.getElementById("chatInput").addEventListener("keypress", (e) => {
        if (e.key === "Enter") submitChatQuery();
    });
});

let currentWeatherData = null;

async function fetchWeatherData(cityName = null) {
    const city = cityName || document.getElementById("cityInput").value.trim() || "Coimbatore";
    
    // Show loading indicators
    document.getElementById("conditionText").innerText = "Analyzing...";
    document.getElementById("chatAnswer").innerText = "Fetching weather intelligence for " + city + "...";

    try {
        const response = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
        if (!response.ok) throw new Error("Failed to fetch weather data");
        
        const data = await response.json();
        currentWeatherData = data;
        renderDashboard(data);
    } catch (err) {
        console.error("API Error:", err);
        document.getElementById("conditionText").innerText = "Connection Error";
        document.getElementById("chatAnswer").innerText = "Error loading weather data. Please ensure server is running.";
    }
}

function renderDashboard(data) {
    if (!data || !data.metrics) return;

    const m = data.metrics;
    const r = data.risk_analysis;
    const recs = data.recommendations;
    const env = data.environmental_intelligence;

    // 1. Real-time Telemetry
    document.getElementById("locationName").innerText = `${data.location} (${data.latitude.toFixed(2)}°, ${data.longitude.toFixed(2)}°)`;
    document.getElementById("tempVal").innerText = m.temperature_c.toFixed(1);
    document.getElementById("feelsLikeVal").innerText = m.feels_like_c.toFixed(1);
    document.getElementById("conditionText").innerText = m.weather_condition;

    document.getElementById("humidityVal").innerText = `${m.relative_humidity}%`;
    document.getElementById("windVal").innerText = `${m.wind_speed_kmh} km/h`;
    document.getElementById("rainVal").innerText = `${m.rain_probability}%`;
    document.getElementById("uvVal").innerText = m.uv_index.toFixed(1);
    document.getElementById("pressureVal").innerText = `${m.pressure_hpa} hPa`;
    document.getElementById("cloudVal").innerText = `${m.cloud_cover}%`;

    // 2. Risk Meter
    const riskScore = r.risk_score || 0;
    const riskLevel = r.risk_level || "LOW";
    
    document.getElementById("riskScoreNum").innerText = riskScore;
    
    const badge = document.getElementById("riskLevelBadge");
    badge.innerText = riskLevel;
    badge.className = `risk-badge risk-level-${riskLevel}`;

    const fill = document.getElementById("meterFill");
    fill.style.width = `${riskScore}%`;
    
    if (riskScore <= 25) fill.style.background = "linear-gradient(90deg, #10b981, #34d399)";
    else if (riskScore <= 50) fill.style.background = "linear-gradient(90deg, #f59e0b, #fbbf24)";
    else if (riskScore <= 75) fill.style.background = "linear-gradient(90deg, #f97316, #f87171)";
    else fill.style.background = "linear-gradient(90deg, #f43f5e, #e11d48)";

    document.getElementById("riskReason").innerText = r.primary_reason || "Optimal weather conditions.";

    // Alerts
    const alertsDiv = document.getElementById("alertsContainer");
    alertsDiv.innerHTML = "";
    if (r.emergency_alerts && r.emergency_alerts.length > 0) {
        r.emergency_alerts.forEach(alert => {
            const box = document.createElement("div");
            box.style.background = "rgba(244, 63, 94, 0.15)";
            box.style.border = "1px solid rgba(244, 63, 94, 0.4)";
            box.style.borderRadius = "10px";
            box.style.padding = "10px 12px";
            box.style.marginTop = "8px";
            box.innerHTML = `
                <div style="font-weight:700; color:#f87171; font-size:0.85rem;">⚠️ ${alert.title}</div>
                <div style="font-size:0.78rem; color:#cbd5e1; margin-top:2px;">${alert.warning}</div>
                <div style="font-size:0.75rem; color:#94a3b8; margin-top:4px; font-style:italic;">Safety: ${alert.safety}</div>
            `;
            alertsDiv.appendChild(box);
        });
    }

    // 3. Daily Summary
    document.getElementById("dailySummaryText").innerText = data.daily_summary || "No summary available.";

    // 4. Outdoor Activities
    const actGrid = document.getElementById("activitiesGrid");
    actGrid.innerHTML = "";
    if (recs.outdoor_activities) {
        recs.outdoor_activities.forEach(act => {
            const card = document.createElement("div");
            card.className = "activity-card";
            card.innerHTML = `
                <div class="activity-header">
                    <span class="activity-name">${act.activity_name}</span>
                    <span class="status-badge status-${act.status}">${act.status}</span>
                </div>
                <div class="activity-reason">${act.reason}</div>
            `;
            actGrid.appendChild(card);
        });
    }

    // 5. Environmental Intelligence
    const envGrid = document.getElementById("envGrid");
    envGrid.innerHTML = `
        <div class="env-box">
            <div class="env-title">☀️ Solar Generation</div>
            <div class="env-val">${env.solar_power_potential}</div>
            <div class="env-desc">${env.solar_details}</div>
        </div>
        <div class="env-box">
            <div class="env-title">💨 Wind Energy</div>
            <div class="env-val">${env.wind_energy_potential}</div>
            <div class="env-desc">${env.wind_details}</div>
        </div>
        <div class="env-box">
            <div class="env-title">🌾 Crop Irrigation</div>
            <div class="env-val">${env.irrigation_need}</div>
            <div class="env-desc">${env.irrigation_details}</div>
        </div>
        <div class="env-box">
            <div class="env-title">🔥 Wildfire Risk</div>
            <div class="env-val" style="color: ${env.wildfire_risk === 'LOW' ? '#34d399' : '#f87171'};">${env.wildfire_risk}</div>
            <div class="env-desc">Power Grid Load: ${env.electricity_demand_impact}</div>
        </div>
    `;

    // 6. 7-Day Forecast
    const forecastScroll = document.getElementById("forecastScroll");
    forecastScroll.innerHTML = "";
    if (data.forecast_7day) {
        data.forecast_7day.forEach(f => {
            const fCard = document.createElement("div");
            fCard.className = "forecast-card";
            fCard.innerHTML = `
                <div class="f-day">${f.day_name}</div>
                <div class="f-cond">${f.weather_condition}</div>
                <div class="f-temp">${f.max_temp_c.toFixed(0)}° / ${f.min_temp_c.toFixed(0)}°C</div>
                <div style="font-size:0.75rem; color:var(--text-muted); margin-top:4px;">☔ ${f.rain_probability}%</div>
            `;
            forecastScroll.appendChild(fCard);
        });
    }

    // 7. Multi-Agent JSON Protocol Payload
    document.getElementById("jsonOutput").innerText = JSON.stringify(data.multi_agent_payload, null, 2);

    // Initial decision answer if present
    if (data.decision_answer) {
        document.getElementById("chatAnswer").innerText = data.decision_answer;
    }
}

async function sendQuickPrompt(promptText) {
    document.getElementById("chatInput").value = promptText;
    await submitChatQuery();
}

async function submitChatQuery() {
    const question = document.getElementById("chatInput").value.trim();
    if (!question) return;

    const city = document.getElementById("cityInput").value.trim() || "Coimbatore";
    document.getElementById("chatAnswer").innerText = "Thinking and analyzing conditions...";

    try {
        const response = await fetch("/api/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ city: city, question: question })
        });
        const data = await response.json();
        document.getElementById("chatAnswer").innerText = data.decision_answer || "No decision generated.";
    } catch (err) {
        document.getElementById("chatAnswer").innerText = "Failed to query Smart Decision Engine.";
    }
}
