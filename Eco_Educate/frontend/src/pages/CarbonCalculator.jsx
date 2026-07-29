import React, { useState } from 'react';
import { Calculator, Car, Zap, Package, Sparkles, CheckCircle2, Utensils, Plane, BarChart3 } from 'lucide-react';
import { calculateCarbon } from '../utils/api';

export default function CarbonCalculator() {
  const [dailyTravelKm, setDailyTravelKm] = useState(20);
  const [travelMode, setTravelMode] = useState('car_petrol');
  const [monthlyElectricityKwh, setMonthlyElectricityKwh] = useState(220);
  const [weeklyPlasticItems, setWeeklyPlasticItems] = useState(12);
  const [dietType, setDietType] = useState('average');
  const [flightsPerYear, setFlightsPerYear] = useState(0);

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCalculate = async (e) => {
    e.preventDefault();
    setLoading(true);
    const res = await calculateCarbon({
      dailyTravelKm: Number(dailyTravelKm),
      travelMode,
      monthlyElectricityKwh: Number(monthlyElectricityKwh),
      weeklyPlasticItems: Number(weeklyPlasticItems),
      dietType,
      flightsPerYear: Number(flightsPerYear)
    });
    setResult(res);
    setLoading(false);
  };

  const getRatingBadgeColor = (color) => {
    switch (color) {
      case 'green': return 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40';
      case 'yellow': return 'bg-yellow-500/20 text-yellow-300 border-yellow-500/40';
      case 'orange': return 'bg-orange-500/20 text-orange-300 border-orange-500/40';
      case 'red': return 'bg-rose-500/20 text-rose-300 border-rose-500/40';
      default: return 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40';
    }
  };

  return (
    <div className="max-w-5xl mx-auto py-8 px-4 sm:px-6 space-y-10">
      
      {/* Header */}
      <div className="text-center space-y-3">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold uppercase tracking-wider">
          <Calculator className="w-4 h-4" />
          <span>Personal Eco-Impact Analytics</span>
        </div>
        <h1 className="text-4xl font-extrabold text-white">Carbon Footprint Calculator</h1>
        <p className="text-slate-300 text-sm max-w-xl mx-auto">
          Calculate your accurate annual carbon footprint across travel, energy, single-use plastic, diet, and flights.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Input Form Column */}
        <div className="lg:col-span-6 bg-forest-950 border border-forest-800 rounded-3xl p-6 sm:p-8 space-y-6 shadow-xl">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-emerald-400" />
            <span>Enter Consumption Factors</span>
          </h2>

          <form onSubmit={handleCalculate} className="space-y-5 text-xs">
            
            {/* Travel Input */}
            <div className="space-y-2">
              <label className="font-bold text-slate-300 flex items-center justify-between">
                <span className="flex items-center gap-1.5"><Car className="w-4 h-4 text-amber-400" /> Daily Travel Distance</span>
                <span className="text-emerald-400 font-extrabold">{dailyTravelKm} km/day</span>
              </label>
              <input
                type="range"
                min="0"
                max="120"
                value={dailyTravelKm}
                onChange={(e) => setDailyTravelKm(e.target.value)}
                className="w-full accent-emerald-500 bg-forest-900 rounded-lg cursor-pointer"
              />
              <select
                value={travelMode}
                onChange={(e) => setTravelMode(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl bg-forest-900 border border-forest-700 text-white font-medium"
              >
                <option value="car_petrol">Petrol / Diesel Car (0.19 kg/km)</option>
                <option value="bike">Motorcycle / Scooter (0.05 kg/km)</option>
                <option value="bus">Public Transit - Bus / Metro (0.04 kg/km)</option>
                <option value="ev">Electric Vehicle EV (0.03 kg/km)</option>
              </select>
            </div>

            {/* Electricity Input */}
            <div className="space-y-2">
              <label className="font-bold text-slate-300 flex items-center justify-between">
                <span className="flex items-center gap-1.5"><Zap className="w-4 h-4 text-yellow-400" /> Monthly Electricity Usage</span>
                <span className="text-emerald-400 font-extrabold">{monthlyElectricityKwh} kWh/mo</span>
              </label>
              <input
                type="range"
                min="10"
                max="1000"
                value={monthlyElectricityKwh}
                onChange={(e) => setMonthlyElectricityKwh(e.target.value)}
                className="w-full accent-emerald-500 bg-forest-900 rounded-lg cursor-pointer"
              />
            </div>

            {/* Single-Use Plastic Input */}
            <div className="space-y-2">
              <label className="font-bold text-slate-300 flex items-center justify-between">
                <span className="flex items-center gap-1.5"><Package className="w-4 h-4 text-cyan-400" /> Weekly Single-Use Plastic Items</span>
                <span className="text-emerald-400 font-extrabold">{weeklyPlasticItems} items/wk</span>
              </label>
              <input
                type="range"
                min="0"
                max="50"
                value={weeklyPlasticItems}
                onChange={(e) => setWeeklyPlasticItems(e.target.value)}
                className="w-full accent-emerald-500 bg-forest-900 rounded-lg cursor-pointer"
              />
            </div>

            {/* Dietary Preference */}
            <div className="space-y-2">
              <label className="font-bold text-slate-300 flex items-center gap-1.5">
                <Utensils className="w-4 h-4 text-rose-400" /> Dietary Style:
              </label>
              <select
                value={dietType}
                onChange={(e) => setDietType(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl bg-forest-900 border border-forest-700 text-white font-medium"
              >
                <option value="meat_heavy">Meat-Heavy (~2,500 kg CO₂e/yr)</option>
                <option value="average">Average Mixed Diet (~1,700 kg CO₂e/yr)</option>
                <option value="vegetarian">Vegetarian (~1,000 kg CO₂e/yr)</option>
                <option value="vegan">Vegan / Plant-Based (~600 kg CO₂e/yr)</option>
              </select>
            </div>

            {/* Flights per Year */}
            <div className="space-y-2">
              <label className="font-bold text-slate-300 flex items-center justify-between">
                <span className="flex items-center gap-1.5"><Plane className="w-4 h-4 text-indigo-400" /> Annual Flights Taken</span>
                <span className="text-emerald-400 font-extrabold">{flightsPerYear} flights/yr</span>
              </label>
              <input
                type="range"
                min="0"
                max="10"
                value={flightsPerYear}
                onChange={(e) => setFlightsPerYear(e.target.value)}
                className="w-full accent-emerald-500 bg-forest-900 rounded-lg cursor-pointer"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3.5 rounded-xl bg-gradient-to-r from-emerald-500 to-forest-600 hover:from-emerald-400 hover:to-forest-500 text-white font-bold text-sm shadow-lg shadow-emerald-500/20 transition-all flex items-center justify-center gap-2"
            >
              <Calculator className="w-4 h-4" />
              <span>{loading ? 'Calculating Footprint...' : 'Calculate Carbon Score'}</span>
            </button>
          </form>
        </div>

        {/* Result & Rating Column */}
        <div className="lg:col-span-6 bg-forest-950 border border-forest-800 rounded-3xl p-6 sm:p-8 flex flex-col justify-between shadow-xl">
          {result ? (
            <div className="space-y-6">
              
              <div className="space-y-2 text-center pb-4 border-b border-forest-800">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Total Estimated Annual Footprint</span>
                <div className="text-4xl font-black text-emerald-400">
                  {result.totalCarbonScoreKg} <span className="text-base font-normal text-slate-300">kg CO₂e/yr</span>
                </div>
                <div className={`inline-block px-3.5 py-1 rounded-full text-xs font-extrabold border ${getRatingBadgeColor(result.ratingColor)}`}>
                  {result.rating}
                </div>
              </div>

              {/* Emissions Breakdown Grid */}
              <div className="space-y-2">
                <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                  <BarChart3 className="w-4 h-4 text-emerald-400" /> Carbon Emissions Breakdown
                </h4>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div className="p-3 rounded-xl bg-forest-900/60 border border-forest-800 flex justify-between items-center">
                    <span className="text-slate-400">Transport:</span>
                    <strong className="text-amber-400 font-bold">{result.annualTravelCo2 ?? 0} kg</strong>
                  </div>
                  <div className="p-3 rounded-xl bg-forest-900/60 border border-forest-800 flex justify-between items-center">
                    <span className="text-slate-400">Power:</span>
                    <strong className="text-yellow-400 font-bold">{result.annualElecCo2 ?? 0} kg</strong>
                  </div>
                  <div className="p-3 rounded-xl bg-forest-900/60 border border-forest-800 flex justify-between items-center">
                    <span className="text-slate-400">Diet:</span>
                    <strong className="text-rose-400 font-bold">{result.annualDietCo2 ?? 0} kg</strong>
                  </div>
                  <div className="p-3 rounded-xl bg-forest-900/60 border border-forest-800 flex justify-between items-center">
                    <span className="text-slate-400">Plastic:</span>
                    <strong className="text-cyan-400 font-bold">{result.annualPlasticCo2 ?? 0} kg</strong>
                  </div>
                  <div className="p-3 rounded-xl bg-forest-900/60 border border-forest-800 flex justify-between items-center col-span-2">
                    <span className="text-slate-400">Flights:</span>
                    <strong className="text-indigo-400 font-bold">{result.annualFlightCo2 ?? 0} kg</strong>
                  </div>
                </div>
              </div>

              {/* Comparison Metric */}
              <div className="p-3 rounded-xl bg-forest-900/40 border border-forest-800 text-xs flex justify-around text-slate-300">
                <div>
                  <span className="text-[10px] text-slate-400 block">Global Average</span>
                  <strong>{result.globalAverageKg || 4700} kg CO₂e</strong>
                </div>
                <div className="border-r border-forest-800"></div>
                <div>
                  <span className="text-[10px] text-slate-400 block">Paris 1.5°C Goal</span>
                  <strong className="text-emerald-400">{result.targetGoalKg || 2000} kg CO₂e</strong>
                </div>
              </div>

              {/* Personalized Suggestions */}
              <div className="space-y-3 pt-2">
                <h4 className="text-xs font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4" /> Recommended Action Steps
                </h4>
                <div className="space-y-2">
                  {result.suggestions?.map((s, idx) => (
                    <div key={idx} className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-xs text-slate-200">
                      {s}
                    </div>
                  ))}
                </div>
              </div>

            </div>
          ) : (
            <div className="h-full flex flex-col items-center justify-center text-center p-8 text-slate-400 space-y-3">
              <Calculator className="w-12 h-12 text-forest-700" />
              <p className="text-xs leading-relaxed">Adjust your travel, energy, plastic, and diet sliders on the left and click "Calculate Carbon Score" to view your personal carbon report.</p>
            </div>
          )}
        </div>

      </div>

    </div>
  );
}
