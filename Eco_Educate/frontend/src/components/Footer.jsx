import React, { useEffect, useState } from 'react';
import { Leaf, Heart, Sparkles, ExternalLink } from 'lucide-react';
import { fetchRandomFact } from '../utils/api';

export default function Footer() {
  const [fact, setFact] = useState('');

  useEffect(() => {
    fetchRandomFact().then(setFact);
  }, []);

  return (
    <footer className="bg-forest-950 border-t border-forest-800/80 text-slate-400 text-sm py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Environmental Fact Widget Banner */}
        <div className="mb-10 p-6 rounded-2xl bg-gradient-to-r from-forest-900/60 to-emerald-950/60 border border-emerald-500/20 shadow-inner flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-3 rounded-xl bg-emerald-500/10 text-emerald-400">
              <Sparkles className="w-6 h-6 animate-pulse" />
            </div>
            <div>
              <span className="text-xs uppercase tracking-wider text-emerald-400 font-bold">Environmental Fact</span>
              <p className="text-slate-200 text-sm font-medium mt-0.5">{fact || "Loading eco fact..."}</p>
            </div>
          </div>
          <button 
            onClick={() => fetchRandomFact().then(setFact)}
            className="text-xs px-3.5 py-2 rounded-lg bg-forest-800 hover:bg-forest-700 text-emerald-300 font-semibold transition-colors shrink-0"
          >
            Next Fact
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <Leaf className="w-6 h-6 text-emerald-400" />
              <span className="text-lg font-bold text-white">EcoGuide AI</span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Empowering global citizens with AI-driven environmental education, climate awareness, and chemical-free natural farming advisory.
            </p>
          </div>

          <div>
            <h4 className="text-sm font-bold text-white uppercase tracking-wider mb-3">Core Modules</h4>
            <ul className="space-y-2 text-xs">
              <li><a href="/chat" className="hover:text-emerald-400 transition-colors">AI Mentor Chat</a></li>
              <li><a href="/learn" className="hover:text-emerald-400 transition-colors">Interactive Climate Learning</a></li>
              <li><a href="/farming" className="hover:text-emerald-400 transition-colors">Natural Farming Advisor</a></li>
              <li><a href="/quiz" className="hover:text-emerald-400 transition-colors">Environmental Quizzes</a></li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-bold text-white uppercase tracking-wider mb-3">Impact Tools</h4>
            <ul className="space-y-2 text-xs">
              <li><a href="/carbon" className="hover:text-emerald-400 transition-colors">Carbon Footprint Calculator</a></li>
              <li><a href="/poster" className="hover:text-emerald-400 transition-colors">Awareness Poster Generator</a></li>
              <li><a href="/dashboard" className="hover:text-emerald-400 transition-colors">Analytics Dashboard</a></li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-bold text-white uppercase tracking-wider mb-3">Tech & AI</h4>
            <p className="text-xs text-slate-400 leading-relaxed mb-2">
              Powered by Groq Llama 3.3, RAG Architecture, Python Flask, and MongoDB.
            </p>
            <span className="inline-block px-2.5 py-1 text-[11px] font-semibold text-emerald-400 bg-emerald-950 border border-emerald-800 rounded-full">
              Production Ready v1.0
            </span>
          </div>
        </div>

        <div className="pt-6 border-t border-forest-900 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-4">
          <p>© {new Date().getFullYear()} EcoGuide AI. Educating for a Sustainable Planet.</p>
          <div className="flex items-center gap-1">
            <span>Built with</span>
            <Heart className="w-3.5 h-3.5 text-emerald-500 fill-emerald-500" />
            <span>for Nature & Future Generations</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
