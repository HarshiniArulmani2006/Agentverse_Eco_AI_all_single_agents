/* ============================================================
   EcoWaste AI – Dashboard JavaScript
   Charts, Game, API Integration, Interactivity
   ============================================================ */

"use strict";

// ─── Constants ───────────────────────────────────────────────
const API = "/api";

const GAME_ITEMS = [
  { label: "🧴 Plastic Bottle", cat: "plastic" },
  { label: "🍌 Banana Peel",    cat: "organic" },
  { label: "📰 Newspaper",      cat: "paper" },
  { label: "🫙 Glass Jar",       cat: "glass" },
  { label: "🥫 Tin Can",         cat: "metal" },
  { label: "📱 Old Phone",       cat: "ewaste" },
  { label: "☢️ Battery",         cat: "hazardous" },
  { label: "🩺 Syringe",         cat: "biomedical" },
  { label: "🧱 Broken Brick",    cat: "construction" },
  { label: "🌿 Grass Clipping",  cat: "organic" },
  { label: "📦 Cardboard Box",   cat: "paper" },
  { label: "🍕 Leftover Food",   cat: "organic" },
  { label: "🖨️ Printer",         cat: "ewaste" },
  { label: "🎨 Paint Can",       cat: "hazardous" },
  { label: "🍾 Wine Bottle",     cat: "glass" },
];

const GAME_BINS = [
  { key: "organic",     label: "Organic",    icon: "🌿", color: "#22c55e" },
  { key: "plastic",     label: "Plastic",    icon: "♻️",  color: "#3b82f6" },
  { key: "paper",       label: "Paper",      icon: "📄", color: "#f59e0b" },
  { key: "glass",       label: "Glass",      icon: "🫙",  color: "#06b6d4" },
  { key: "metal",       label: "Metal",      icon: "🥫", color: "#6366f1" },
  { key: "ewaste",      label: "E-Waste",    icon: "💻", color: "#8b5cf6" },
  { key: "hazardous",   label: "Hazardous",  icon: "⚠️", color: "#ef4444" },
  { key: "biomedical",  label: "Biomedical", icon: "🏥", color: "#f43f5e" },
];

const RECYCLING_FACTS = [
  "♻️ Recycling one aluminum can saves enough energy to run a TV for 3 hours.",
  "🌳 Recycling 1 ton of paper saves 17 trees and 7,000 gallons of water.",
  "🌍 Plastic takes 400+ years to decompose in landfill.",
  "💡 Glass can be recycled infinitely without loss of quality.",
  "📱 Mining gold from e-waste is 13× more efficient than mining ore.",
  "🌿 Composting reduces methane from landfill by up to 50%.",
  "🔋 One battery can contaminate 1 million liters of water if dumped in soil.",
  "🏭 Industrial waste-to-energy converts 85% of waste volume to energy.",
];

const LEADERBOARD_DATA = [
  { rank: "🥇", name: "Priya Sharma",    pts: 980 },
  { rank: "🥈", name: "Arjun Mehta",     pts: 840 },
  { rank: "🥉", name: "Kavitha Raj",     pts: 720 },
  { rank: "4",  name: "Ravi Nair",       pts: 650 },
  { rank: "5",  name: "Sunita Patel",    pts: 590 },
];

// ─── State ────────────────────────────────────────────────────
let charts = {};
let gameState = { score: 0, streak: 0, currentItem: null, itemQueue: [], answered: 0 };
let currentAnalysis = null;

// ─── DOM Ready ────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  initGame();
  initChat();
  loadDashboard();
  attachFormHandler();
  initQuickQuestions();
  initJsonExport();
});

// ─── Tab Navigation ──────────────────────────────────────────
function initTabs() {
  const tabs = document.querySelectorAll(".nav-tab");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));
      tab.classList.add("active");
      document.getElementById(tab.dataset.tab)?.classList.add("active");
      if (tab.dataset.tab === "tab-bins") refreshBins();
      if (tab.dataset.tab === "tab-forecast") loadForecast();
    });
  });
}

// ─── Dashboard Load ──────────────────────────────────────────
async function loadDashboard() {
  try {
    const data = await apiFetch("/dashboard-data");
    renderDashboardStats(data);
    renderWasteDistributionChart(data.community_analytics.household_waste_breakdown);
    renderSustainabilityScores(data.sample_analysis.sustainability_scores);
    renderBins(data.smart_bins.smart_bins);
    renderRecommendations(data.sample_analysis.sustainability_recommendations);
    renderEcoChallenges(data.eco_challenges);
    renderEcoBadges(data.eco_badges);
    renderLeaderboard();
  } catch (err) {
    console.warn("Dashboard load fallback:", err);
    renderDashboardStatsFallback();
  }
}

function renderDashboardStats(data) {
  const ca = data.community_analytics;
  setEl("stat-recycle-rate",     ca.recycling_rate_pct + "%");
  setEl("stat-zero-waste",       ca.zero_waste_progress_pct + "%");
  setEl("stat-annual-waste",     ca.annual_waste_kg + " kg");
  setEl("stat-urgent-bins",      data.smart_bins.route_optimization?.urgent_collections || 0);
}

function renderDashboardStatsFallback() {
  setEl("stat-recycle-rate", "42%");
  setEl("stat-zero-waste",   "48%");
  setEl("stat-annual-waste", "657 kg");
  setEl("stat-urgent-bins",  "3");
  renderWasteDistributionChart({organic:35, plastic:20, paper:18, glass:5, metal:4, ewaste:3, other:15});
  renderSustainabilityScores({waste_score:74,recycling_score:81,environmental_score:62,sustainability_score:72,circular_economy_score:68,carbon_reduction_score:79,score_confidence:91});
}

// ─── Waste Distribution Donut ────────────────────────────────
function renderWasteDistributionChart(breakdown) {
  const ctx = document.getElementById("chartDistribution")?.getContext("2d");
  if (!ctx) return;
  if (charts.distribution) charts.distribution.destroy();

  const labels = Object.keys(breakdown).map(k => k.charAt(0).toUpperCase() + k.slice(1));
  const data   = Object.values(breakdown);
  const colors = ["#22c55e","#3b82f6","#f59e0b","#06b6d4","#6366f1","#8b5cf6","#94a3b8","#f97316"];

  charts.distribution = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels,
      datasets: [{ data, backgroundColor: colors, borderColor: "rgba(5,13,10,0.8)", borderWidth: 3, hoverOffset: 8 }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { position: "right", labels: { color: "#86efac", font: { family: "Inter", size: 11 }, padding: 12 } },
        tooltip: { callbacks: { label: ctx => ` ${ctx.label}: ${ctx.parsed}%` } }
      },
      cutout: "68%"
    }
  });
}

// ─── Sustainability Score Rings ──────────────────────────────
function renderSustainabilityScores(scores) {
  const scoreMap = {
    "ring-waste":    { val: scores.waste_score,            color: "#22c55e", label: "Waste" },
    "ring-recycling":{ val: scores.recycling_score,        color: "#3b82f6", label: "Recycling" },
    "ring-env":      { val: scores.environmental_score,    color: "#10b981", label: "Environment" },
    "ring-sust":     { val: scores.sustainability_score,   color: "#f59e0b", label: "Sustainability" },
    "ring-circular": { val: scores.circular_economy_score, color: "#8b5cf6", label: "Circular Economy" },
    "ring-carbon":   { val: scores.carbon_reduction_score, color: "#06b6d4", label: "Carbon Reduction" },
  };

  for (const [id, cfg] of Object.entries(scoreMap)) {
    const el = document.getElementById(id);
    if (!el) continue;
    const val      = Math.round(cfg.val || 0);
    const circ     = 2 * Math.PI * 40;
    const offset   = circ - (val / 100) * circ;
    const svg      = el.querySelector(".score-ring-fill");
    const valEl    = el.querySelector(".score-ring-value");
    if (svg) {
      svg.style.stroke           = cfg.color;
      svg.style.strokeDasharray  = circ;
      svg.style.strokeDashoffset = circ;     // start hidden
      setTimeout(() => { svg.style.strokeDashoffset = offset; }, 100);
    }
    if (valEl) valEl.textContent = val;
  }
}

// ─── Bin Rendering ────────────────────────────────────────────
function renderBins(bins) {
  const wrap = document.getElementById("bins-container");
  if (!wrap) return;
  wrap.innerHTML = bins.map(b => {
    const fillH = Math.round(b.fill_level_pct * 1.2) + "px"; // visual height max 120
    const urg   = b.overflow_prediction.urgent_collection;
    return `
      <div class="bin-card">
        <div class="bin-header">
          <div>
            <div class="bin-id">${b.bin_id}</div>
            <div class="bin-type">${b.waste_type.toUpperCase()}</div>
          </div>
          <span class="badge ${badgeClassForLevel(b.status)}">${b.status}</span>
        </div>
        <div class="bin-fill-visual">
          <div class="bin-fill-inner" style="height:${b.fill_level_pct}%;background:${b.status_color};opacity:0.85;"></div>
        </div>
        <div class="bin-info">
          <div class="bin-pct" style="color:${b.status_color}">${b.fill_level_pct}%</div>
          <div class="bin-location">📍 ${b.location}</div>
          <div style="font-size:0.72rem;color:var(--text-dim);margin-bottom:6px;">🌡️ ${b.temperature_c}°C &nbsp;|&nbsp; ${b.bin_health}</div>
          ${urg ? `<div class="bin-overflow-warn">⚡ Overflow in ~${b.overflow_prediction.hours_until_overflow}h</div>` : `<div style="font-size:0.7rem;color:var(--text-dim);">🕐 ~${b.overflow_prediction.hours_until_overflow}h to full</div>`}
        </div>
      </div>`;
  }).join("");
}

async function refreshBins() {
  try {
    const data = await apiFetch("/smart-bins");
    renderBins(data.smart_bins);
    renderRouteOptimization(data.route_optimization);
  } catch(e) {}
}

function renderRouteOptimization(routes) {
  const el = document.getElementById("route-info");
  if (!el || !routes) return;
  const s = routes.optimization_savings;
  el.innerHTML = `
    <div class="grid-3" style="gap:12px;">
      <div class="stat-item"><div class="stat-icon" style="background:rgba(34,197,94,0.1)">⛽</div><div class="stat-body"><div class="stat-val" style="color:#22c55e">${s.fuel_saved_litres}L</div><div class="stat-lbl">Fuel Saved</div></div></div>
      <div class="stat-item"><div class="stat-icon" style="background:rgba(6,182,212,0.1)">🌍</div><div class="stat-body"><div class="stat-val" style="color:#06b6d4">${s.co2_saved_kg}kg</div><div class="stat-lbl">CO₂ Saved</div></div></div>
      <div class="stat-item"><div class="stat-icon" style="background:rgba(245,158,11,0.1)">⏱️</div><div class="stat-body"><div class="stat-val" style="color:#f59e0b">${s.time_saved_minutes}min</div><div class="stat-lbl">Time Saved</div></div></div>
    </div>
    <div class="xai-box" style="margin-top:14px;">${routes.xai_reason}</div>`;
}

// ─── Waste Analysis Form ─────────────────────────────────────
function attachFormHandler() {
  const form = document.getElementById("analysis-form");
  if (!form) return;
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const btn = document.getElementById("analyze-btn");
    const loader = document.getElementById("analysis-loader");
    btn.disabled = true;
    loader.classList.add("visible");

    const payload = {
      waste_type:  document.getElementById("input-waste").value.trim(),
      quantity_kg: parseFloat(document.getElementById("input-qty").value) || 1.0,
      location:    document.getElementById("input-location").value.trim() || "City",
      source:      document.getElementById("input-source").value,
    };

    try {
      const data = await apiFetch("/analyze", "POST", payload);
      currentAnalysis = data;
      renderAnalysisResult(data);
      // Switch to analyze tab
      document.querySelector('[data-tab="tab-analyze"]')?.click();
    } catch(err) {
      showToast("❌ Analysis failed. Please try again.", "error");
    } finally {
      btn.disabled = false;
      loader.classList.remove("visible");
    }
  });
}

function renderAnalysisResult(data) {
  const cls  = data.classification;
  const rec  = data.recycling;
  const env  = data.environmental_impact;
  const carb = data.carbon_footprint;
  const risk = data.risk_assessment;
  const sc   = data.sustainability_scores;

  // Show result section
  document.getElementById("classification-result")?.classList.add("visible");

  // Header
  setEl("res-icon",     cls.category_icon);
  setEl("res-type",     `Input: "${cls.input_waste_type}"`);
  setEl("res-category", cls.category_label);
  setEl("res-bin",      cls.bin_type);
  setEl("res-conf",     cls.confidence + "%");
  setEl("res-xai",      cls.xai_reason);

  // Recyclability badges
  const badges = [];
  if (rec.is_recyclable)  badges.push(`<span class="badge badge-green">♻️ Recyclable</span>`);
  if (rec.is_compostable) badges.push(`<span class="badge badge-green">🌿 Compostable</span>`);
  if (rec.is_reusable)    badges.push(`<span class="badge badge-blue">🔄 Reusable</span>`);
  if (rec.energy_recovery)badges.push(`<span class="badge badge-amber">⚡ Energy Recovery</span>`);
  if (cls.is_toxic)       badges.push(`<span class="badge badge-red">☠️ Toxic</span>`);
  if (cls.is_flammable)   badges.push(`<span class="badge badge-orange">🔥 Flammable</span>`);
  setHTML("res-badges", badges.join(""));

  // Efficiency
  setEl("res-eff", rec.recycling_efficiency + "%");
  const effBar = document.getElementById("res-eff-bar");
  if (effBar) { effBar.style.width = "0"; setTimeout(() => { effBar.style.width = rec.recycling_efficiency + "%"; }, 100); }

  // Can become
  const products = (cls.can_become || []).map(p => `<span class="product-tag">${p}</span>`).join("");
  setHTML("res-products", products || '<span class="badge badge-slate">No direct products</span>');

  // Recycling steps
  const steps = (rec.recycling_steps || []).map(s => `<li>${s}</li>`).join("");
  setHTML("res-steps", steps);

  // Upcycling ideas
  const upcycle = (rec.upcycling_ideas || []).map(u => `<div class="upcycle-card">${u}</div>`).join("");
  setHTML("res-upcycle", upcycle || '<p style="color:var(--text-dim);font-size:0.83rem">No upcycling ideas available.</p>');

  // Risk
  setEl("res-risk-score", risk.risk_score.toFixed(1));
  setEl("res-risk-level", risk.risk_level);
  setEl("res-risk-xai",   risk.xai_reason);
  const riskEl = document.getElementById("res-risk-score");
  if (riskEl) riskEl.style.color = risk.risk_color;

  // Emergency alerts
  renderEmergencyAlerts(data.emergency_alerts);

  // Pollution sources
  renderPollutionSources(data.pollution_sources);

  // Carbon comparison
  renderCarbonComparison(carb.comparison);
  setEl("res-carbon-xai", carb.xai_reason);

  // Environmental impact
  renderEnvironmentalImpact(env);

  // Sustainability scores
  renderSustainabilityScores(sc);
  setEl("res-sust-xai", sc.xai_reason);

  // Circular economy
  setEl("res-circular-insight", data.circular_economy_insight);

  // Recommendations
  renderRecommendations(data.sustainability_recommendations);

  // Multi-agent payload
  const payloadEl = document.getElementById("multi-agent-json");
  if (payloadEl) payloadEl.textContent = JSON.stringify(data.multi_agent_payload, null, 2);

  showToast(`✅ Analyzed: ${cls.category_label} (${cls.confidence}% confidence)`, "success");
}

function renderEmergencyAlerts(alerts) {
  const el = document.getElementById("emergency-alerts");
  if (!el) return;
  if (!alerts || alerts.length === 0) {
    el.innerHTML = `<div class="alert alert-low"><div class="alert-icon">✅</div><div class="alert-body"><div class="alert-title">No Emergency Alerts</div><div class="alert-message">This waste type poses no immediate emergency hazards under standard conditions.</div></div></div>`;
    return;
  }
  el.innerHTML = alerts.map(a => `
    <div class="alert alert-${a.severity === 'CRITICAL' ? 'critical' : 'high'}">
      <div class="alert-icon">${a.severity === 'CRITICAL' ? '🚨' : '⚠️'}</div>
      <div class="alert-body">
        <div class="alert-title">${a.type}</div>
        <div class="alert-message">${a.message}</div>
        <div style="margin-top:8px;font-size:0.8rem;font-weight:600;color:var(--amber)">💡 ${a.recommendation}</div>
      </div>
    </div>`).join("");
}

function renderPollutionSources(sources) {
  const el = document.getElementById("pollution-sources");
  if (!el || !sources) return;
  el.innerHTML = sources.map(s => `
    <div style="margin-bottom:10px;">
      <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
        <span style="font-size:0.82rem">${s.source}</span>
        <span class="badge ${badgeClassForRisk(s.risk_level)}">${s.confidence}%</span>
      </div>
      <div class="progress-bar-wrap">
        <div class="progress-bar-fill" style="width:0;background:${colorForRisk(s.risk_level)}" data-target="${s.confidence}"></div>
      </div>
    </div>`).join("");
  // Animate bars
  setTimeout(() => {
    el.querySelectorAll(".progress-bar-fill").forEach(bar => {
      bar.style.width = bar.dataset.target + "%";
    });
  }, 100);
}

function renderCarbonComparison(comparison) {
  const el = document.getElementById("carbon-comparison");
  if (!el || !comparison) return;
  el.innerHTML = comparison.map(c => `
    <div class="carbon-row ${c.is_best ? 'best' : ''}">
      <span class="carbon-method">${c.method}</span>
      <span class="carbon-val" style="color:${c.is_best ? 'var(--green-400)' : 'var(--text-dim)'}">${c.emissions_kg > 0 ? '+' : ''}${c.emissions_kg} kg CO₂e</span>
      <span style="font-size:0.75rem">${c.label}</span>
    </div>`).join("");
}

function renderEnvironmentalImpact(env) {
  const el = document.getElementById("env-impact-grid");
  if (!el || !env.dimensions) return;
  setEl("env-score-val", env.environmental_score);
  setEl("env-level",     env.impact_level);
  setEl("env-xai",       env.xai_reason);

  const dimLabels = {
    air:"🌬️ Air", water:"💧 Water", soil:"🌱 Soil", wildlife:"🦁 Wildlife",
    marine:"🐠 Marine", climate:"🌡️ Climate", health:"🏥 Human Health", biodiversity:"🌿 Biodiversity"
  };

  el.innerHTML = Object.entries(env.dimensions).map(([dim, val]) => {
    const col = val.level === "HIGH" ? "var(--red)" : val.level === "MODERATE" ? "var(--amber)" : "var(--green-500)";
    return `
      <div class="impact-cell">
        <div class="impact-dim">${dimLabels[dim] || dim}</div>
        <div class="impact-score" style="color:${col}">${val.score}</div>
        <div class="impact-level" style="color:${col}">${val.level}</div>
        <div style="font-size:0.69rem;color:var(--text-dim);margin-top:4px;line-height:1.4">${val.description}</div>
      </div>`;
  }).join("");
}

function renderRecommendations(recs) {
  const el = document.getElementById("sustainability-recs");
  if (!el || !recs) return;
  el.innerHTML = recs.map(r => `
    <div style="display:flex;align-items:flex-start;gap:10px;padding:10px 14px;background:var(--bg-glass);border:1px solid var(--border);border-radius:var(--radius-sm);font-size:0.83rem;color:var(--text-secondary);">
      ${r}
    </div>`).join("");
}

// ─── Forecast ────────────────────────────────────────────────
async function loadForecast() {
  try {
    const data = await apiFetch("/forecast");
    renderForecastCharts(data);
    renderAnomalies(data.anomalies);
    renderCommunityAnalytics(data.community_analytics);
  } catch(e) { console.warn("Forecast load error:", e); }
}

function renderForecastCharts(data) {
  const daily = data.forecast.daily_7day || [];
  const monthly = data.forecast.monthly_12month || [];

  // Daily chart
  const dCtx = document.getElementById("chartDaily")?.getContext("2d");
  if (dCtx) {
    if (charts.daily) charts.daily.destroy();
    charts.daily = new Chart(dCtx, {
      type: "bar",
      data: {
        labels: daily.map(d => d.day.slice(0,3)),
        datasets: [{
          label: "Waste (kg)",
          data: daily.map(d => d.estimated_kg),
          backgroundColor: daily.map(d => d.label === "Weekend Peak" ? "rgba(245,158,11,0.6)" : "rgba(34,197,94,0.5)"),
          borderColor:     daily.map(d => d.label === "Weekend Peak" ? "#f59e0b" : "#22c55e"),
          borderWidth: 2, borderRadius: 6,
        }]
      },
      options: chartDefaults("Estimated Daily Waste Generation (kg)")
    });
  }

  // Monthly chart
  const mCtx = document.getElementById("chartMonthly")?.getContext("2d");
  if (mCtx) {
    if (charts.monthly) charts.monthly.destroy();
    charts.monthly = new Chart(mCtx, {
      type: "line",
      data: {
        labels: monthly.map(m => m.month),
        datasets: [{
          label: "Monthly Waste (kg)",
          data: monthly.map(m => m.estimated_kg),
          borderColor: "#22c55e", backgroundColor: "rgba(34,197,94,0.1)",
          borderWidth: 2, fill: true, tension: 0.4,
          pointBackgroundColor: "#22c55e", pointRadius: 4,
        }]
      },
      options: chartDefaults("Monthly Waste Forecast (kg)")
    });
  }
}

function renderAnomalies(anomalies) {
  const el = document.getElementById("anomalies-list");
  if (!el) return;
  el.innerHTML = anomalies.map(a => `
    <div class="alert alert-moderate" style="margin-bottom:10px;">
      <div class="alert-icon">📊</div>
      <div class="alert-body">
        <div class="alert-title">${a.anomaly}</div>
        <div class="alert-message">${a.description} — ${a.probable_cause}</div>
        <div style="margin-top:6px;font-size:0.78rem;color:var(--green-400)">💡 ${a.recommendation}</div>
        <div style="margin-top:4px;font-size:0.72rem;color:var(--text-dim)">Confidence: ${a.confidence}%</div>
      </div>
    </div>`).join("");
}

function renderCommunityAnalytics(ca) {
  const el = document.getElementById("community-stats");
  if (!el) return;
  el.innerHTML = `
    <div class="grid-3" style="gap:12px;">
      <div class="stat-item"><div class="stat-icon" style="background:rgba(34,197,94,0.1)">♻️</div><div class="stat-body"><div class="stat-val" style="color:#22c55e">${ca.recycling_rate_pct}%</div><div class="stat-lbl">Recycling Rate</div></div></div>
      <div class="stat-item"><div class="stat-icon" style="background:rgba(245,158,11,0.1)">🏗️</div><div class="stat-body"><div class="stat-val" style="color:#f59e0b">${ca.landfill_rate_pct}%</div><div class="stat-lbl">Landfill Rate</div></div></div>
      <div class="stat-item"><div class="stat-icon" style="background:rgba(16,185,129,0.1)">🌿</div><div class="stat-body"><div class="stat-val" style="color:#10b981">${ca.compost_rate_pct}%</div><div class="stat-lbl">Compost Rate</div></div></div>
    </div>
    <div style="margin-top:16px;font-size:0.83rem;color:var(--text-dim);">
      Zero Waste Progress: <strong style="color:var(--green-400)">${ca.zero_waste_progress_pct}%</strong> &nbsp;|&nbsp; 
      Plastic Reduction Target: <strong style="color:var(--amber)">${ca.plastic_reduction_target_pct}%</strong>
    </div>`;
}

// ─── Eco Challenges & Badges ─────────────────────────────────
function renderEcoChallenges(challenges) {
  const el = document.getElementById("eco-challenges");
  if (!el) return;
  el.innerHTML = (challenges || []).map(c => `
    <div class="card" style="padding:20px;cursor:pointer;" onclick="joinChallenge('${c.challenge}', ${c.reward_points})">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
        <div style="font-weight:700;font-size:0.9rem">${c.challenge}</div>
        <span class="badge badge-green">+${c.reward_points} pts</span>
      </div>
      <div style="font-size:0.8rem;color:var(--text-dim);margin-bottom:12px">${c.description}</div>
      <button class="btn-secondary" style="font-size:0.78rem;padding:7px 16px">Join Challenge →</button>
    </div>`).join("");
}

function renderEcoBadges(badges) {
  const el = document.getElementById("eco-badges");
  if (!el) return;
  el.innerHTML = (badges || []).map(b => `
    <div class="badge-card">
      <div class="badge-card-icon">${b.badge.split(" ")[0]}</div>
      <div class="badge-card-name">${b.badge.split(" ").slice(1).join(" ")}</div>
      <div class="badge-card-pts">⭐ ${b.points_required} pts</div>
      <div class="badge-card-desc">${b.description}</div>
    </div>`).join("");
}

function renderLeaderboard() {
  const el = document.getElementById("leaderboard");
  if (!el) return;
  el.innerHTML = LEADERBOARD_DATA.map(r => `
    <div class="leaderboard-row">
      <div class="leaderboard-rank">${r.rank}</div>
      <div class="leaderboard-name">${r.name}</div>
      <div class="leaderboard-pts">🌿 ${r.pts} pts</div>
    </div>`).join("");
}

function joinChallenge(name, pts) {
  showToast(`🌿 Joined challenge: ${name}! Earn ${pts} points on completion.`, "success");
}

// ─── Waste Segregation Game ──────────────────────────────────
function initGame() {
  gameState = { score: 0, streak: 0, currentItem: null, itemQueue: [...shuffleArray(GAME_ITEMS)], answered: 0 };
  renderGameBins();
  nextGameItem();
  setEl("game-score", "0");
}

function renderGameBins() {
  const el = document.getElementById("game-bins");
  if (!el) return;
  el.innerHTML = GAME_BINS.map(b => `
    <div class="game-bin" id="bin-${b.key}" style="background:${b.color}18;border-color:${b.color}44;"
         ondragover="event.preventDefault();this.classList.add('drag-over')"
         ondragleave="this.classList.remove('drag-over')"
         ondrop="handleDrop(event,'${b.key}')">
      <div class="game-bin-icon">${b.icon}</div>
      <div class="game-bin-label">${b.label}</div>
    </div>`).join("");
}

function nextGameItem() {
  if (gameState.itemQueue.length === 0) {
    gameState.itemQueue = [...shuffleArray(GAME_ITEMS)];
  }
  gameState.currentItem = gameState.itemQueue.shift();
  const el = document.getElementById("current-waste-item");
  if (el) {
    el.innerHTML = `
      <div class="waste-item" draggable="true" id="drag-item"
           ondragstart="event.dataTransfer.setData('text','waste');document.getElementById('drag-item').classList.add('dragging')"
           ondragend="document.getElementById('drag-item').classList.remove('dragging')">
        ${gameState.currentItem.label}
      </div>`;
  }
  hideFeedback();
  showFact();
}

function handleDrop(event, binKey) {
  event.preventDefault();
  document.querySelectorAll(".game-bin").forEach(b => b.classList.remove("drag-over"));
  if (!gameState.currentItem) return;

  const correct = gameState.currentItem.cat === binKey;
  gameState.answered++;

  if (correct) {
    gameState.score += 10 + (gameState.streak * 2);
    gameState.streak++;
    showFeedback(true, `✅ Correct! ${gameState.currentItem.label} goes in the ${binKey} bin. +${10 + ((gameState.streak - 1) * 2)} points!`);
    highlightBin(binKey, true);
  } else {
    const correctBin = GAME_BINS.find(b => b.key === gameState.currentItem.cat);
    gameState.streak = 0;
    showFeedback(false, `❌ Not quite! ${gameState.currentItem.label} should go in the ${correctBin?.label || gameState.currentItem.cat} bin.`);
    highlightBin(gameState.currentItem.cat, false);
  }

  setEl("game-score", gameState.score);
  setEl("game-streak", `🔥 Streak: ${gameState.streak}`);
  setTimeout(nextGameItem, 1800);
}

function highlightBin(binKey, correct) {
  const bin = document.getElementById(`bin-${binKey}`);
  if (!bin) return;
  bin.style.transform = "scale(1.08)";
  bin.style.borderColor = correct ? "#22c55e" : "#ef4444";
  setTimeout(() => { bin.style.transform = ""; bin.style.borderColor = ""; }, 1500);
}

function showFeedback(correct, msg) {
  const el = document.getElementById("game-feedback");
  if (!el) return;
  el.className = `game-feedback ${correct ? 'correct' : 'wrong'}`;
  el.textContent = msg;
}

function hideFeedback() {
  const el = document.getElementById("game-feedback");
  if (el) el.className = "game-feedback";
}

function showFact() {
  const el = document.getElementById("recycling-fact");
  if (!el) return;
  const fact = RECYCLING_FACTS[Math.floor(Math.random() * RECYCLING_FACTS.length)];
  el.textContent = fact;
}

// ─── Conversational AI Chat ───────────────────────────────────
function initChat() {
  const input = document.getElementById("chat-input");
  const btn   = document.getElementById("chat-send");
  if (!input || !btn) return;

  const send = async () => {
    const q = input.value.trim();
    if (!q) return;
    addChatMsg(q, "user");
    input.value = "";

    const wasteType = document.getElementById("input-waste")?.value || "plastic bottle";
    try {
      const data = await apiFetch("/query", "POST", { query: q, waste_type: wasteType, quantity_kg: 1.0, source: "residential" });
      addChatMsg(data.answer, "agent");
    } catch {
      addChatMsg("I'm having trouble connecting. Please try again.", "agent");
    }
  };

  btn.addEventListener("click", send);
  input.addEventListener("keydown", e => { if (e.key === "Enter") send(); });
}

function addChatMsg(text, role) {
  const el = document.getElementById("chat-messages");
  if (!el) return;
  const div = document.createElement("div");
  div.className = `chat-msg ${role}`;
  div.innerHTML = `
    <div class="chat-avatar">${role === "agent" ? "🌿" : "👤"}</div>
    <div class="chat-bubble">${text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}</div>`;
  el.appendChild(div);
  el.scrollTop = el.scrollHeight;
}

// ─── Quick Question Buttons ──────────────────────────────────
function initQuickQuestions() {
  document.querySelectorAll(".quick-question").forEach(btn => {
    btn.addEventListener("click", () => {
      const q = btn.dataset.q;
      const chatInput = document.getElementById("chat-input");
      if (chatInput) {
        chatInput.value = q;
        document.getElementById("chat-send")?.click();
        document.querySelector('[data-tab="tab-chat"]')?.click();
      }
    });
  });
}

// ─── JSON Export ─────────────────────────────────────────────
function initJsonExport() {
  document.getElementById("export-json-btn")?.addEventListener("click", () => {
    if (!currentAnalysis) { showToast("Please run an analysis first.", "info"); return; }
    const blob = new Blob([JSON.stringify(currentAnalysis.multi_agent_payload, null, 2)], { type: "application/json" });
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement("a");
    a.href = url; a.download = "ecowaste_multi_agent_payload.json"; a.click();
    URL.revokeObjectURL(url);
    showToast("📥 Multi-Agent JSON exported!", "success");
  });

  document.getElementById("copy-json-btn")?.addEventListener("click", () => {
    const el = document.getElementById("multi-agent-json");
    if (el) {
      navigator.clipboard.writeText(el.textContent);
      showToast("📋 JSON copied to clipboard!", "success");
    }
  });
}

// ─── Chart Defaults ──────────────────────────────────────────
function chartDefaults(title) {
  return {
    responsive: true, maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: { backgroundColor: "#0a1612", borderColor: "rgba(34,197,94,0.3)", borderWidth: 1, titleColor: "#86efac", bodyColor: "#f0fdf4" },
    },
    scales: {
      x: { ticks: { color: "#6b7280", font: { size: 11 } }, grid: { color: "rgba(255,255,255,0.04)" } },
      y: { ticks: { color: "#6b7280", font: { size: 11 } }, grid: { color: "rgba(255,255,255,0.06)" } }
    }
  };
}

// ─── Toast Notifications ─────────────────────────────────────
function showToast(msg, type = "info") {
  const existing = document.getElementById("toast");
  if (existing) existing.remove();
  const toast = document.createElement("div");
  toast.id = "toast";
  const colors = { success: "#22c55e", error: "#ef4444", info: "#3b82f6" };
  Object.assign(toast.style, {
    position: "fixed", bottom: "24px", right: "24px", zIndex: "9999",
    background: "#0a1612", border: `1px solid ${colors[type] || colors.info}`,
    borderRadius: "12px", padding: "14px 20px", color: "#f0fdf4",
    fontSize: "0.87rem", maxWidth: "380px", boxShadow: "0 8px 32px rgba(0,0,0,0.5)",
    animation: "fadeSlideIn 0.3s ease",
  });
  toast.textContent = msg;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3500);
}

// ─── Helpers ─────────────────────────────────────────────────
async function apiFetch(path, method = "GET", body = null) {
  const opts = {
    method,
    headers: { "Content-Type": "application/json" },
    ...(body ? { body: JSON.stringify(body) } : {})
  };
  const res = await fetch(API + path, opts);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

function setEl(id, val) {
  const el = document.getElementById(id);
  if (el) el.textContent = val;
}

function setHTML(id, val) {
  const el = document.getElementById(id);
  if (el) el.innerHTML = val;
}

function badgeClassForLevel(status) {
  if (!status) return "badge-slate";
  const s = status.toLowerCase();
  if (s === "overflow" || s === "critical") return "badge-red";
  if (s === "high")     return "badge-orange";
  if (s === "partial")  return "badge-amber";
  return "badge-green";
}

function badgeClassForRisk(level) {
  if (!level) return "badge-slate";
  if (level === "HIGH")     return "badge-red";
  if (level === "MODERATE") return "badge-amber";
  return "badge-green";
}

function colorForRisk(level) {
  if (level === "HIGH")     return "var(--red)";
  if (level === "MODERATE") return "var(--amber)";
  return "var(--green-500)";
}

function shuffleArray(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
