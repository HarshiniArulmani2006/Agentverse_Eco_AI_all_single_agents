import React, { useEffect, useState } from 'react';
import { LayoutDashboard, Users, MessageSquare, Award, Calculator, Sprout, TrendingUp, Search, PieChart } from 'lucide-react';
import { fetchDashboardStats } from '../utils/api';

export default function Dashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchDashboardStats().then(setStats);
  }, []);

  if (!stats) return <div className="p-12 text-center text-slate-400">Loading system analytics dashboard...</div>;

  const m = stats.metrics;

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-10">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold uppercase tracking-wider mb-2">
            <LayoutDashboard className="w-4 h-4" />
            <span>Platform Overview & Analytics</span>
          </div>
          <h1 className="text-3xl font-extrabold text-white">EcoGuide AI System Dashboard</h1>
        </div>

        <div className="flex items-center gap-2 text-xs">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping"></span>
          <span className="text-emerald-400 font-bold uppercase tracking-wider">Live System Active</span>
        </div>
      </div>

      {/* Top Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        
        <div className="p-5 rounded-2xl bg-forest-950 border border-forest-800 space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-bold uppercase">Total Users</span>
            <Users className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">{m.total_users}</div>
          <span className="text-[11px] text-emerald-400 font-medium">Registered eco learners</span>
        </div>

        <div className="p-5 rounded-2xl bg-forest-950 border border-forest-800 space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-bold uppercase">Questions Asked</span>
            <MessageSquare className="w-5 h-5 text-teal-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">{m.total_questions_asked}</div>
          <span className="text-[11px] text-teal-400 font-medium">AI RAG interactions</span>
        </div>

        <div className="p-5 rounded-2xl bg-forest-950 border border-forest-800 space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-bold uppercase">Quiz Tests</span>
            <Award className="w-5 h-5 text-amber-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">{m.quiz_participation}</div>
          <span className="text-[11px] text-amber-400 font-medium">Badges awarded</span>
        </div>

        <div className="p-5 rounded-2xl bg-forest-950 border border-forest-800 space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-bold uppercase">Carbon Audits</span>
            <Calculator className="w-5 h-5 text-cyan-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">{m.carbon_calculations}</div>
          <span className="text-[11px] text-cyan-400 font-medium">Footprint checks</span>
        </div>

        <div className="p-5 rounded-2xl bg-forest-950 border border-forest-800 space-y-2">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-bold uppercase">Farming Queries</span>
            <Sprout className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="text-3xl font-extrabold text-white">{m.farming_queries}</div>
          <span className="text-[11px] text-emerald-400 font-medium">Organic crop queries</span>
        </div>

      </div>

      {/* Analytics Breakdown Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Most Searched Environmental Topics Bar Analytics */}
        <div className="lg:col-span-7 bg-forest-950 border border-forest-800 rounded-3xl p-6 sm:p-8 space-y-6 shadow-xl">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <Search className="w-5 h-5 text-emerald-400" />
              <span>Most Searched Environmental Topics</span>
            </h3>
            <span className="text-xs text-slate-400">Search Volume %</span>
          </div>

          <div className="space-y-4">
            {stats.topSearchedTopics.map((item, idx) => (
              <div key={idx} className="space-y-1.5">
                <div className="flex justify-between text-xs font-bold">
                  <span className="text-slate-200">{item.topic}</span>
                  <span className="text-emerald-400">{item.searches} queries ({item.percentage}%)</span>
                </div>
                <div className="w-full bg-forest-900 h-3 rounded-full overflow-hidden border border-forest-800">
                  <div
                    className="bg-gradient-to-r from-emerald-500 to-teal-400 h-full rounded-full transition-all duration-500"
                    style={{ width: `${item.percentage * 2.5}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quiz Badges & Carbon Impact Pie Breakdown */}
        <div className="lg:col-span-5 space-y-6">
          
          {/* Badges Distribution Card */}
          <div className="bg-forest-950 border border-forest-800 rounded-3xl p-6 space-y-4 shadow-xl">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Award className="w-4 h-4 text-amber-400" />
              <span>Quiz Badges Earned Breakdown</span>
            </h3>
            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-300 font-bold flex justify-between">
                <span>Earth Protector</span>
                <span>{stats.quizStats.badgesAwarded["Earth Protector"]}</span>
              </div>
              <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 font-bold flex justify-between">
                <span>Green Warrior</span>
                <span>{stats.quizStats.badgesAwarded["Green Warrior"]}</span>
              </div>
              <div className="p-3 rounded-xl bg-teal-500/10 border border-teal-500/20 text-teal-300 font-bold flex justify-between">
                <span>Eco Learner</span>
                <span>{stats.quizStats.badgesAwarded["Eco Learner"]}</span>
              </div>
              <div className="p-3 rounded-xl bg-slate-800 border border-slate-700 text-slate-300 font-bold flex justify-between">
                <span>Eco Beginner</span>
                <span>{stats.quizStats.badgesAwarded["Eco Beginner"]}</span>
              </div>
            </div>
          </div>

          {/* Carbon Footprint Ratings Breakdown Card */}
          <div className="bg-forest-950 border border-forest-800 rounded-3xl p-6 space-y-4 shadow-xl">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <Calculator className="w-4 h-4 text-cyan-400" />
              <span>Carbon Footprint Ratings Breakdown</span>
            </h3>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between items-center text-slate-300">
                <span>Average User Carbon Footprint:</span>
                <strong className="text-emerald-400 text-sm">{stats.carbonAnalytics.averageCarbonScoreKg} kg CO₂e</strong>
              </div>
              <div className="flex justify-between items-center text-slate-300">
                <span>Moderate Impact Users:</span>
                <strong className="text-amber-400">{stats.carbonAnalytics.moderateImpactPercentage}</strong>
              </div>
              <div className="flex justify-between items-center text-slate-300">
                <span>High Impact Users:</span>
                <strong className="text-rose-400">{stats.carbonAnalytics.highImpactPercentage}</strong>
              </div>
            </div>
          </div>

        </div>

      </div>

    </div>
  );
}
