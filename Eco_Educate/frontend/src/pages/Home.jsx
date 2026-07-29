import React from 'react';
import { Link } from 'react-router-dom';
import { Leaf, MessageSquare, Sprout, ShieldAlert, Sun, Droplet, Globe, Award, ArrowRight, CheckCircle2, Sparkles, Compass } from 'lucide-react';
import { translations } from '../utils/translations';

export default function Home({ language }) {
  const t = translations[language] || translations.en;

  const cards = [
    {
      title: "Climate Change",
      desc: "Understand rising global temperatures, greenhouse gas emissions, and actionable mitigation strategies.",
      icon: Sun,
      color: "from-amber-500/20 to-orange-500/20 text-amber-400 border-amber-500/30",
      link: "/learn#climate-change"
    },
    {
      title: "Pollution Control",
      desc: "Explore causes and prevention of air, water, soil, and noise contamination in urban and rural habitats.",
      icon: ShieldAlert,
      color: "from-rose-500/20 to-red-500/20 text-rose-400 border-rose-500/30",
      link: "/learn#pollution"
    },
    {
      title: "Biodiversity",
      desc: "Discover ecosystem services, species protection, and habitat conservation practices worldwide.",
      icon: Leaf,
      color: "from-emerald-500/20 to-green-500/20 text-emerald-400 border-emerald-500/30",
      link: "/learn#biodiversity"
    },
    {
      title: "Natural Farming",
      desc: "Learn chemical-free farming, composting recipes, Jeevamrutham bio-tonic, and natural pest control.",
      icon: Sprout,
      color: "from-teal-500/20 to-emerald-600/20 text-teal-300 border-teal-500/30",
      link: "/farming"
    },
    {
      title: "Water Conservation",
      desc: "Master rainwater harvesting, drip irrigation efficiency, and household greywater recycling.",
      icon: Droplet,
      color: "from-cyan-500/20 to-blue-500/20 text-cyan-400 border-cyan-500/30",
      link: "/learn#water-conservation"
    },
    {
      title: "Renewable Energy",
      desc: "Dive into solar photovoltaic power, wind turbines, energy efficiency, and clean grid integration.",
      icon: Globe,
      color: "from-yellow-500/20 to-amber-500/20 text-yellow-300 border-yellow-500/30",
      link: "/learn#renewable-energy"
    }
  ];

  return (
    <div className="space-y-16 py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      
      {/* Hero Section */}
      <section className="relative rounded-3xl overflow-hidden bg-gradient-to-br from-forest-900 via-forest-950 to-emerald-950 border border-forest-800 shadow-2xl p-8 sm:p-12 lg:p-16">
        {/* Glow backdrop decorative elements */}
        <div className="absolute -top-24 -right-24 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="absolute -bottom-24 -left-24 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl pointer-events-none"></div>

        <div className="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          <div className="lg:col-span-7 space-y-6">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold uppercase tracking-wider">
              <Sparkles className="w-4 h-4" />
              <span>Next-Gen Environmental Mentor</span>
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-white tracking-tight leading-tight">
              {t.heroTitle}
            </h1>

            <p className="text-slate-300 text-lg leading-relaxed max-w-2xl">
              {t.heroSubtitle} Ask questions in simple language, calculate your carbon impact, take dynamic quizzes, and learn natural farming techniques.
            </p>

            <div className="flex flex-wrap gap-4 pt-2">
              <Link
                to="/chat"
                className="flex items-center gap-2.5 px-6 py-3.5 rounded-xl bg-gradient-to-r from-emerald-500 to-forest-600 hover:from-emerald-400 hover:to-forest-500 text-white font-bold shadow-lg shadow-emerald-500/25 transition-all transform hover:-translate-y-0.5"
              >
                <MessageSquare className="w-5 h-5" />
                <span>{t.askAiBtn}</span>
                <ArrowRight className="w-4 h-4" />
              </Link>

              <Link
                to="/carbon"
                className="flex items-center gap-2.5 px-6 py-3.5 rounded-xl bg-forest-900/80 hover:bg-forest-800 border border-forest-700 text-slate-100 font-bold transition-all"
              >
                <span>{t.calcFootprintBtn}</span>
              </Link>
            </div>

            <div className="pt-6 border-t border-forest-800/80 grid grid-cols-3 gap-4 text-slate-400 text-xs">
              <div>
                <span className="text-lg font-bold text-emerald-400 block">7+ Topics</span>
                <span>Interactive Learning</span>
              </div>
              <div>
                <span className="text-lg font-bold text-emerald-400 block">RAG Engine</span>
                <span>Groq Llama 3 AI</span>
              </div>
              <div>
                <span className="text-lg font-bold text-emerald-400 block">2 Languages</span>
                <span>English & தமிழ் Support</span>
              </div>
            </div>
          </div>

          <div className="lg:col-span-5 relative">
            <div className="relative rounded-2xl bg-forest-900/90 border border-forest-700 p-6 shadow-xl space-y-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-400">
                  <Leaf className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-white">EcoGuide AI Interactive Assistant</h3>
                  <span className="text-[11px] text-emerald-400 font-medium">Ready to educate & assist</span>
                </div>
              </div>

              <div className="bg-forest-950 p-4 rounded-xl border border-forest-800 text-xs text-slate-300 space-y-2">
                <p className="text-emerald-400 font-semibold">User: "How do I make compost at home naturally?"</p>
                <p className="text-slate-200">
                  <strong className="text-white">EcoGuide AI:</strong> Layer dry leaves (Browns) and kitchen peels (Greens) in a 3:1 ratio. Keep moist and stir weekly for rich dark humus in 45 days!
                </p>
              </div>

              <div className="flex items-center justify-between text-xs text-slate-400 pt-2">
                <span className="flex items-center gap-1"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> Actionable Tips</span>
                <span className="flex items-center gap-1"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> Beginner Friendly</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Mission Statement */}
      <section className="text-center max-w-3xl mx-auto space-y-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold uppercase">
          <Compass className="w-4 h-4" />
          <span>Our Vision & Mission</span>
        </div>
        <h2 className="text-3xl font-extrabold text-white">Democratizing Environmental & Agricultural Knowledge</h2>
        <p className="text-slate-300 leading-relaxed text-sm">
          EcoGuide AI bridges the gap between complex climate science and daily human action. By combining conversational artificial intelligence with retrieval-augmented environmental knowledge, we make sustainable living and organic farming simple, accessible, and rewarding for everyone.
        </p>
      </section>

      {/* Quick Access Cards */}
      <section className="space-y-8">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-white">Explore Environmental Topics</h2>
            <p className="text-slate-400 text-xs mt-1">Select a core domain to begin interactive learning or ask the AI mentor.</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {cards.map((card, idx) => {
            const Icon = card.icon;
            return (
              <Link
                key={idx}
                to={card.link}
                className={`group p-6 rounded-2xl bg-gradient-to-b ${card.color} border bg-forest-950/60 hover:bg-forest-900/80 transition-all duration-300 shadow-md hover:shadow-emerald-500/10 flex flex-col justify-between`}
              >
                <div className="space-y-4">
                  <div className="w-12 h-12 rounded-xl bg-forest-900/90 border border-forest-700 flex items-center justify-center group-hover:scale-110 transition-transform">
                    <Icon className="w-6 h-6" />
                  </div>
                  <h3 className="text-lg font-bold text-white group-hover:text-emerald-300 transition-colors">
                    {card.title}
                  </h3>
                  <p className="text-xs text-slate-300 leading-relaxed">{card.desc}</p>
                </div>

                <div className="pt-4 mt-4 border-t border-white/5 flex items-center text-xs font-semibold text-emerald-400 group-hover:translate-x-1 transition-transform">
                  <span>Learn Topic Details</span>
                  <ArrowRight className="w-4 h-4 ml-1" />
                </div>
              </Link>
            );
          })}
        </div>
      </section>

      {/* Environmental Banner & Call to Action */}
      <section className="rounded-3xl bg-gradient-to-r from-emerald-900 via-forest-900 to-teal-950 p-8 sm:p-12 border border-emerald-500/30 flex flex-col md:flex-row items-center justify-between gap-8 shadow-xl">
        <div className="space-y-3 max-w-2xl">
          <span className="text-xs font-bold uppercase tracking-wider text-amber-300 bg-amber-400/10 px-2.5 py-1 rounded border border-amber-400/20">
            Interactive Eco Quiz
          </span>
          <h2 className="text-3xl font-extrabold text-white">Test Your Green Knowledge & Earn Badges</h2>
          <p className="text-slate-200 text-sm">
            Challenge yourself with dynamic environmental questions. Earn badges like <strong className="text-emerald-300">Green Warrior</strong> and <strong className="text-emerald-300">Earth Protector</strong> to share with friends!
          </p>
        </div>
        <Link
          to="/quiz"
          className="px-8 py-4 rounded-xl bg-white hover:bg-slate-100 text-forest-950 font-extrabold shadow-lg transition-all transform hover:scale-105 shrink-0 flex items-center gap-2"
        >
          <Award className="w-5 h-5 text-emerald-600" />
          <span>Start Eco Quiz Now</span>
        </Link>
      </section>

    </div>
  );
}
