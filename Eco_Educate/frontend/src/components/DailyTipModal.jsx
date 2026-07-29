import React, { useEffect, useState } from 'react';
import { Lightbulb, X, CheckCircle } from 'lucide-react';
import { fetchDailyTip } from '../utils/api';

export default function DailyTipModal() {
  const [dailyTip, setDailyTip] = useState(null);
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    fetchDailyTip().then(setDailyTip);
  }, []);

  if (!dailyTip || !isVisible) return null;

  return (
    <div className="bg-gradient-to-r from-emerald-900/90 via-forest-900/90 to-teal-900/90 border-b border-emerald-500/30 px-4 py-3 shadow-md relative">
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-1.5 rounded-lg bg-emerald-400/20 text-emerald-300 shrink-0">
            <Lightbulb className="w-5 h-5 text-amber-300 animate-bounce" />
          </div>
          <div className="text-xs sm:text-sm">
            <span className="font-bold text-amber-300 mr-2 uppercase tracking-wider text-[11px] bg-amber-400/10 px-2 py-0.5 rounded border border-amber-400/30">
              Daily Eco Tip ({dailyTip.category})
            </span>
            <span className="text-slate-100 font-medium">{dailyTip.tip}</span>
          </div>
        </div>

        <button
          onClick={() => setIsVisible(false)}
          className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-forest-800/60 transition-colors shrink-0"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
