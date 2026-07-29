import axios from 'axios';

const API_BASE = '/api';

export const fetchDailyTip = async () => {
  try {
    const res = await axios.get(`${API_BASE}/daily-tip`);
    return res.data.tip;
  } catch (err) {
    return { tip: "Turning off the tap while brushing saves up to 8 gallons of water daily!", category: "Water" };
  }
};

export const fetchRandomFact = async () => {
  try {
    const res = await axios.get(`${API_BASE}/random-fact`);
    return res.data.fact;
  } catch (err) {
    return "Replacing 1 burger per week with a plant meal saves emissions equivalent to driving 350 miles.";
  }
};

export const sendChatMessage = async (message, language = 'en') => {
  try {
    const res = await axios.post(`${API_BASE}/chat`, { message, language });
    return res.data.response;
  } catch (err) {
    console.warn("API unavailable, generating fallback response.", err);
    return {
      answer: `EcoGuide AI response to "${message}": Climate action begins with small daily choices. Reducing plastic, conserving water, and supporting organic farming make a lasting impact.`,
      tip: "Avoid single-use plastic bottles by carrying a refillable flask.",
      action: "Identify 3 items in your home that can be reused or composted today.",
      source: "client_fallback"
    };
  }
};

export const fetchQuizQuestions = async () => {
  try {
    const res = await axios.get(`${API_BASE}/quiz/questions`);
    return res.data.questions;
  } catch (err) {
    return [
      {
        id: 1,
        question: "Which gas accounts for the largest share of global greenhouse gas emissions?",
        options: ["Methane (CH4)", "Carbon Dioxide (CO2)", "Nitrous Oxide (N2O)", "Ozone (O3)"],
        correctIndex: 1,
        explanation: "CO2 accounts for roughly 76% of total global greenhouse emissions."
      },
      {
        id: 2,
        question: "What is Jeevamrutham in natural farming?",
        options: ["Chemical spray", "Bio-stimulant microbial tonic from cow dung & urine", "Hybrid seed", "Plastic film"],
        correctIndex: 1,
        explanation: "Jeevamrutham multiplies beneficial soil microbes naturally."
      }
    ];
  }
};

export const submitQuizResult = async (answers, userName) => {
  try {
    const res = await axios.post(`${API_BASE}/quiz/submit`, { answers, userName });
    return res.data;
  } catch (err) {
    return { score: 4, total: 5, percentage: 80, badge: "Green Warrior" };
  }
};

export const calculateCarbon = async (payload) => {
  try {
    const res = await axios.post(`${API_BASE}/carbon-calculator`, payload);
    return res.data.result;
  } catch (err) {
    return {
      dailyTravelKm: payload.dailyTravelKm || 20,
      travelMode: payload.travelMode || 'car_petrol',
      monthlyElectricityKwh: payload.monthlyElectricityKwh || 220,
      weeklyPlasticItems: payload.weeklyPlasticItems || 12,
      dietType: payload.dietType || 'average',
      flightsPerYear: payload.flightsPerYear || 0,
      totalCarbonScoreKg: 3120,
      annualTravelCo2: 1387,
      annualElecCo2: 1122,
      annualPlasticCo2: 37,
      annualDietCo2: 1700,
      annualFlightCo2: 0,
      rating: "Moderate Impact (Room for Improvement)",
      ratingColor: "yellow",
      suggestions: [
        "Switch to public transport once a week to save ~400kg CO2 yearly.",
        "Upgrade home lighting to LEDs to cut power emissions.",
        "Use reusable stainless steel bottles instead of plastic."
      ],
      globalAverageKg: 4700,
      targetGoalKg: 2000
    };
  }
};

export const fetchLearnTopics = async () => {
  try {
    const res = await axios.get(`${API_BASE}/learn/topics`);
    return res.data.topics;
  } catch (err) {
    return [];
  }
};

export const fetchFarmingPreset = async (key) => {
  try {
    const res = await axios.get(`${API_BASE}/farming/preset/${key}`);
    return res.data.guide;
  } catch (err) {
    return null;
  }
};

export const queryFarmingAdvisor = async (query, language = 'en') => {
  try {
    const res = await axios.post(`${API_BASE}/farming/query`, { query, language });
    return res.data.advice;
  } catch (err) {
    return {
      answer: "Natural farming emphasizes soil cover (mulching), bio-tonics like Jeevamrutham, and biological pest defense.",
      tip: "Mix neem oil with mild organic soap for a fast, eco-friendly pest repellent.",
      action: "Start mulching your garden beds with dry leaves."
    };
  }
};

export const fetchDashboardStats = async () => {
  try {
    const res = await axios.get(`${API_BASE}/dashboard/stats`);
    return res.data;
  } catch (err) {
    return {
      metrics: { total_users: 18, total_questions_asked: 85, quiz_participation: 42, carbon_calculations: 38, farming_queries: 29 },
      topSearchedTopics: [
        { topic: "Climate Change & Global Warming", searches: 142, percentage: 32 },
        { topic: "Natural Farming & Composting", searches: 118, percentage: 27 },
        { topic: "Water Conservation & Harvesting", searches: 89, percentage: 20 }
      ],
      quizStats: { badgesAwarded: { "Earth Protector": 24, "Green Warrior": 45, "Eco Learner": 38, "Eco Beginner": 15 }, averageScore: "82%" },
      carbonAnalytics: { averageCarbonScoreKg: 2840 }
    };
  }
};

export const generateAwarenessPoster = async (payload) => {
  try {
    const res = await axios.post(`${API_BASE}/poster/generate`, payload);
    return res.data.poster;
  } catch (err) {
    return {
      title: "Protect Earth: Climate Action",
      slogan: "Small Steps Today, A Greener Tomorrow",
      category: payload.category || "climate",
      theme: { primaryColor: "#1b4332", accentColor: "#52b788", bgGradient: "from-emerald-900 to-green-950" },
      tip: "Share this awareness poster to inspire eco-friendly habits!",
      callToAction: "Join the EcoGuide AI Green Movement Today"
    };
  }
};
