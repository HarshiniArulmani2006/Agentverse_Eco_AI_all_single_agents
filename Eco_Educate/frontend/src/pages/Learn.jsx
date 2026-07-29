import React, { useEffect, useState } from 'react';
import { fetchLearnTopics } from '../utils/api';
import { BookOpen, Sun, Thermometer, Wind, Leaf, Droplet, Recycle, CloudSun, CheckCircle, AlertTriangle, ShieldCheck, Sparkles, ChevronRight } from 'lucide-react';

export default function Learn() {
  const [topics, setTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState(null);

  useEffect(() => {
    fetchLearnTopics().then(data => {
      setTopics(data);
      if (data.length > 0) setSelectedTopic(data[0]);
    });
  }, []);

  const getIcon = (iconName) => {
    switch (iconName) {
      case 'Sun': return Sun;
      case 'Thermometer': return Thermometer;
      case 'Wind': return Wind;
      case 'Leaf': return Leaf;
      case 'Droplet': return Droplet;
      case 'Recycle': return Recycle;
      default: return CloudSun;
    }
  };

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-10">
      
      {/* Header Banner */}
      <div className="text-center max-w-3xl mx-auto space-y-4">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold uppercase tracking-wider">
          <BookOpen className="w-4 h-4" />
          <span>Interactive Environmental Knowledge Hub</span>
        </div>
        <h1 className="text-4xl font-extrabold text-white">Learn Environmental Science & Sustainability</h1>
        <p className="text-slate-300 text-sm leading-relaxed">
          Explore structured definitions, root causes, ecological effects, global prevention strategies, and real-world success examples across 7 core topics.
        </p>
      </div>

      {/* Main Layout Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Topics Drawer Navigation */}
        <div className="lg:col-span-4 space-y-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 px-2">Select Educational Topic</h3>
          <div className="space-y-2">
            {topics.map((t) => {
              const Icon = getIcon(t.icon);
              const isSelected = selectedTopic?.id === t.id;
              return (
                <button
                  key={t.id}
                  onClick={() => setSelectedTopic(t)}
                  className={`w-full text-left p-4 rounded-2xl border transition-all flex items-center justify-between group ${
                    isSelected
                      ? 'bg-gradient-to-r from-forest-800 to-emerald-900 border-emerald-500/50 shadow-lg text-white'
                      : 'bg-forest-950/70 hover:bg-forest-900/60 border-forest-800 text-slate-300'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div className={`p-2.5 rounded-xl ${isSelected ? 'bg-emerald-500/20 text-emerald-300' : 'bg-forest-900 text-slate-400 group-hover:text-emerald-400'}`}>
                      <Icon className="w-5 h-5" />
                    </div>
                    <div>
                      <h4 className="text-sm font-bold">{t.title}</h4>
                      <span className="text-[11px] text-slate-400">{t.category}</span>
                    </div>
                  </div>
                  <ChevronRight className={`w-5 h-5 transition-transform ${isSelected ? 'text-emerald-400 translate-x-1' : 'text-slate-500'}`} />
                </button>
              );
            })}
          </div>
        </div>

        {/* Right Topic Detail Card */}
        <div className="lg:col-span-8">
          {selectedTopic ? (
            <div className="bg-forest-950 border border-forest-800/80 rounded-3xl p-6 sm:p-8 space-y-8 shadow-xl">
              
              {/* Card Header */}
              <div className="space-y-3 pb-6 border-b border-forest-800">
                <span className="text-xs uppercase tracking-wider font-bold text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20">
                  {selectedTopic.category} Module
                </span>
                <h2 className="text-3xl font-bold text-white">{selectedTopic.title}</h2>
                <div className="p-4 rounded-2xl bg-forest-900/80 border border-forest-800 text-slate-200 text-sm leading-relaxed">
                  <strong className="text-emerald-300 block mb-1 text-xs uppercase tracking-wider">Definition:</strong>
                  {selectedTopic.definition}
                </div>
              </div>

              {/* Grid of Causes & Effects */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                
                {/* Causes Section */}
                <div className="p-5 rounded-2xl bg-rose-500/5 border border-rose-500/20 space-y-3">
                  <h3 className="text-sm font-bold text-rose-300 flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4 text-rose-400" />
                    Primary Causes
                  </h3>
                  <ul className="space-y-2 text-xs text-slate-300">
                    {selectedTopic.causes.map((c, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-rose-400 shrink-0 mt-1.5"></span>
                        <span>{c}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Effects Section */}
                <div className="p-5 rounded-2xl bg-amber-500/5 border border-amber-500/20 space-y-3">
                  <h3 className="text-sm font-bold text-amber-300 flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4 text-amber-400" />
                    Ecological Impacts & Effects
                  </h3>
                  <ul className="space-y-2 text-xs text-slate-300">
                    {selectedTopic.effects.map((e, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-amber-400 shrink-0 mt-1.5"></span>
                        <span>{e}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Prevention Section */}
              <div className="p-5 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 space-y-3">
                <h3 className="text-sm font-bold text-emerald-300 flex items-center gap-2">
                  <ShieldCheck className="w-5 h-5 text-emerald-400" />
                  Prevention & Mitigation Strategies
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {selectedTopic.prevention.map((p, idx) => (
                    <div key={idx} className="p-3 rounded-xl bg-forest-900/60 border border-forest-800 flex items-start gap-2 text-xs text-slate-200">
                      <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                      <span>{p}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Real-World Examples */}
              <div className="p-5 rounded-2xl bg-teal-500/10 border border-teal-500/20 space-y-3">
                <h3 className="text-sm font-bold text-teal-300 flex items-center gap-2">
                  <Sparkles className="w-5 h-5 text-teal-400" />
                  Real-World Case Studies & Examples
                </h3>
                <div className="space-y-2 text-xs text-slate-200">
                  {selectedTopic.examples.map((ex, idx) => (
                    <div key={idx} className="p-3 rounded-xl bg-forest-900/40 border border-teal-500/20 italic">
                      "{ex}"
                    </div>
                  ))}
                </div>
              </div>

            </div>
          ) : (
            <div className="p-12 text-center text-slate-400">Loading educational module...</div>
          )}
        </div>
      </div>

    </div>
  );
}
