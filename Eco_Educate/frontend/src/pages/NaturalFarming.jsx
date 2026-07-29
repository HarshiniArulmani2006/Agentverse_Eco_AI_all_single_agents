import React, { useState } from 'react';
import { Sprout, Droplet, Sun, ShieldCheck, Beaker, Calendar, Search, ArrowRight, CheckCircle2, Sparkles, Leaf } from 'lucide-react';
import { fetchFarmingPreset, queryFarmingAdvisor } from '../utils/api';

export default function NaturalFarming({ language }) {
  const [activeTab, setActiveTab] = useState('tomatoes'); // tomatoes, compost, pest_control
  const [customQuery, setCustomQuery] = useState('');
  const [queryLoading, setQueryLoading] = useState(false);
  const [advisorResponse, setAdvisorResponse] = useState(null);

  const handlePresetClick = async (tabKey) => {
    setActiveTab(tabKey);
    setAdvisorResponse(null);
  };

  const handleCustomSubmit = async (e) => {
    e.preventDefault();
    if (!customQuery.trim() || queryLoading) return;
    setQueryLoading(true);
    const res = await queryFarmingAdvisor(customQuery, language);
    setAdvisorResponse(res);
    setQueryLoading(false);
  };

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-12">
      
      {/* Page Header */}
      <div className="text-center max-w-3xl mx-auto space-y-4">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold uppercase tracking-wider">
          <Sprout className="w-4 h-4" />
          <span>Zero-Chemical Natural Farming Advisor</span>
        </div>
        <h1 className="text-4xl font-extrabold text-white">Natural & Organic Agriculture Guide</h1>
        <p className="text-slate-300 text-sm leading-relaxed">
          Nourish soil microbes, control agricultural pests organically, and grow healthy chemical-free crops using traditional bio-preparations like Jeevamrutham and Neem bio-sprays.
        </p>
      </div>

      {/* Preset Guides Quick Switcher */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-4xl mx-auto">
        <button
          onClick={() => handlePresetClick('tomatoes')}
          className={`p-5 rounded-2xl border text-left flex items-center gap-4 transition-all ${
            activeTab === 'tomatoes' && !advisorResponse
              ? 'bg-gradient-to-r from-forest-800 to-emerald-900 border-emerald-500 text-white shadow-lg'
              : 'bg-forest-950/80 border-forest-800 text-slate-300 hover:bg-forest-900'
          }`}
        >
          <div className="p-3 rounded-xl bg-emerald-500/20 text-emerald-400 shrink-0">
            <Sprout className="w-6 h-6" />
          </div>
          <div>
            <h3 className="font-bold text-sm">How to Grow Tomatoes</h3>
            <span className="text-xs text-slate-400">Natural crop care & stakes</span>
          </div>
        </button>

        <button
          onClick={() => handlePresetClick('compost')}
          className={`p-5 rounded-2xl border text-left flex items-center gap-4 transition-all ${
            activeTab === 'compost' && !advisorResponse
              ? 'bg-gradient-to-r from-forest-800 to-emerald-900 border-emerald-500 text-white shadow-lg'
              : 'bg-forest-950/80 border-forest-800 text-slate-300 hover:bg-forest-900'
          }`}
        >
          <div className="p-3 rounded-xl bg-amber-500/20 text-amber-400 shrink-0">
            <Leaf className="w-6 h-6" />
          </div>
          <div>
            <h3 className="font-bold text-sm">How to Make Compost</h3>
            <span className="text-xs text-slate-400">Browns to greens ratio</span>
          </div>
        </button>

        <button
          onClick={() => handlePresetClick('pest_control')}
          className={`p-5 rounded-2xl border text-left flex items-center gap-4 transition-all ${
            activeTab === 'pest_control' && !advisorResponse
              ? 'bg-gradient-to-r from-forest-800 to-emerald-900 border-emerald-500 text-white shadow-lg'
              : 'bg-forest-950/80 border-forest-800 text-slate-300 hover:bg-forest-900'
          }`}
        >
          <div className="p-3 rounded-xl bg-teal-500/20 text-teal-400 shrink-0">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h3 className="font-bold text-sm">Control Pests Naturally</h3>
            <span className="text-xs text-slate-400">Neem oil & Jeevamrutham</span>
          </div>
        </button>
      </div>

      {/* Interactive Custom Farming Question Form */}
      <div className="max-w-3xl mx-auto p-6 rounded-3xl bg-forest-900/60 border border-forest-800 space-y-4">
        <h3 className="text-sm font-bold text-white flex items-center gap-2">
          <Search className="w-4 h-4 text-emerald-400" />
          Ask Natural Farming Advisor Any Crop / Pest Question:
        </h3>
        <form onSubmit={handleCustomSubmit} className="flex items-center gap-3">
          <input
            type="text"
            value={customQuery}
            onChange={(e) => setCustomQuery(e.target.value)}
            placeholder="e.g. How do I protect eggplant from borers organically?"
            className="flex-1 px-5 py-3.5 rounded-xl bg-forest-950 border border-forest-700 text-white text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
          <button
            type="submit"
            disabled={!customQuery.trim() || queryLoading}
            className="px-6 py-3.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-sm disabled:opacity-50 transition-all flex items-center gap-2"
          >
            {queryLoading ? 'Searching...' : 'Get Advice'}
          </button>
        </form>
      </div>

      {/* Advisor Custom Answer Display */}
      {advisorResponse && (
        <div className="max-w-4xl mx-auto p-6 rounded-3xl bg-emerald-950/80 border border-emerald-500/40 space-y-4 shadow-xl">
          <span className="text-xs font-bold uppercase tracking-wider text-emerald-300 bg-emerald-400/20 px-3 py-1 rounded-full">
            AI Farming Advisor Response
          </span>
          <div className="space-y-3 text-sm text-slate-100">
            <div>
              <strong className="text-emerald-400 block text-xs uppercase tracking-wider mb-1">Recommended Practices & Explanation:</strong>
              <p className="leading-relaxed">{advisorResponse.answer}</p>
            </div>
            <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 text-xs text-amber-200">
              <strong className="text-amber-300 block mb-0.5">Organic Farming Tip:</strong>
              {advisorResponse.tip}
            </div>
            <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-xs text-emerald-200">
              <strong className="text-emerald-300 block mb-0.5">Immediate Action Step:</strong>
              {advisorResponse.action}
            </div>
          </div>
        </div>
      )}

      {/* Preset Content Details */}
      {!advisorResponse && (
        <div className="max-w-5xl mx-auto bg-forest-950 border border-forest-800 rounded-3xl p-6 sm:p-10 space-y-8 shadow-xl">
          
          {activeTab === 'tomatoes' && (
            <div className="space-y-6">
              <div className="flex items-center gap-3 pb-4 border-b border-forest-800">
                <Sprout className="w-8 h-8 text-emerald-400" />
                <div>
                  <h2 className="text-2xl font-bold text-white">Natural Tomato Cultivation Guide</h2>
                  <p className="text-xs text-slate-400">High-yield chemical-free techniques</p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
                <div className="p-5 rounded-2xl bg-forest-900/60 border border-forest-800 space-y-2">
                  <span className="text-xs uppercase tracking-wider font-bold text-emerald-400 flex items-center gap-1.5">
                    <Sun className="w-4 h-4" /> Soil & Sun Requirements
                  </span>
                  <p className="text-slate-200 text-xs leading-relaxed">
                    Well-drained loamy soil rich in organic humus (pH 6.0 - 6.8). Plant in full sunlight (6-8 hours daily).
                  </p>
                </div>

                <div className="p-5 rounded-2xl bg-forest-900/60 border border-forest-800 space-y-2">
                  <span className="text-xs uppercase tracking-wider font-bold text-emerald-400 flex items-center gap-1.5">
                    <Beaker className="w-4 h-4" /> Organic Fertilizers
                  </span>
                  <p className="text-slate-200 text-xs leading-relaxed">
                    Apply Jeevamrutham liquid bio-tonic near roots every 14 days. Top dress with vermicompost during flowering stage.
                  </p>
                </div>

                <div className="p-5 rounded-2xl bg-forest-900/60 border border-forest-800 space-y-2">
                  <span className="text-xs uppercase tracking-wider font-bold text-teal-300 flex items-center gap-1.5">
                    <ShieldCheck className="w-4 h-4" /> Natural Pesticides
                  </span>
                  <p className="text-slate-200 text-xs leading-relaxed">
                    Spray Cold-pressed Neem oil (5ml + 2ml liquid soap per liter of water). Use Agniastra spray for severe leaf caterpillars.
                  </p>
                </div>

                <div className="p-5 rounded-2xl bg-forest-900/60 border border-forest-800 space-y-2">
                  <span className="text-xs uppercase tracking-wider font-bold text-cyan-300 flex items-center gap-1.5">
                    <Droplet className="w-4 h-4" /> Water Requirements & Mulching
                  </span>
                  <p className="text-slate-200 text-xs leading-relaxed">
                    Deep watering twice a week directly at base level. Maintain 2 inches of dry straw mulch to lock soil moisture.
                  </p>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'compost' && (
            <div className="space-y-6">
              <div className="flex items-center gap-3 pb-4 border-b border-forest-800">
                <Leaf className="w-8 h-8 text-amber-400" />
                <div>
                  <h2 className="text-2xl font-bold text-white">Aerobic Kitchen Scraps Composting</h2>
                  <p className="text-xs text-slate-400">Transform organic waste into black gold humus</p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="p-5 rounded-2xl bg-amber-500/10 border border-amber-500/20 space-y-3">
                  <h3 className="text-sm font-bold text-amber-300">Browns (Carbon Sources - 75%)</h3>
                  <ul className="text-xs text-slate-200 space-y-1.5">
                    <li>• Dry tree leaves and dry lawn grass</li>
                    <li>• Unprinted cardboard scraps & egg cartons</li>
                    <li>• Sawdust, wood chips, dry twigs</li>
                  </ul>
                </div>

                <div className="p-5 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 space-y-3">
                  <h3 className="text-sm font-bold text-emerald-300">Greens (Nitrogen Sources - 25%)</h3>
                  <ul className="text-xs text-slate-200 space-y-1.5">
                    <li>• Vegetable and fruit peels</li>
                    <li>• Coffee grounds & tea bags</li>
                    <li>• Fresh green leaves & plant clippings</li>
                  </ul>
                </div>
              </div>

              <div className="p-5 rounded-2xl bg-forest-900/60 border border-forest-800 space-y-3">
                <h3 className="text-sm font-bold text-white">Simple 4-Step Composting Process:</h3>
                <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 text-xs text-slate-300">
                  <div className="p-3 bg-forest-950 rounded-xl border border-forest-800">
                    <strong className="text-emerald-400 block mb-1">1. Base Layer</strong>
                    Coarse twigs at bin bottom for air circulation.
                  </div>
                  <div className="p-3 bg-forest-950 rounded-xl border border-forest-800">
                    <strong className="text-emerald-400 block mb-1">2. Layering</strong>
                    Alternate 3 inches of Browns with 1 inch Greens.
                  </div>
                  <div className="p-3 bg-forest-950 rounded-xl border border-forest-800">
                    <strong className="text-emerald-400 block mb-1">3. Moisture</strong>
                    Sprinkle water so pile feels like a damp sponge.
                  </div>
                  <div className="p-3 bg-forest-950 rounded-xl border border-forest-800">
                    <strong className="text-emerald-400 block mb-1">4. Aerate</strong>
                    Turn pile every 7 days; compost ready in 45 days!
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'pest_control' && (
            <div className="space-y-6">
              <div className="flex items-center gap-3 pb-4 border-b border-forest-800">
                <ShieldCheck className="w-8 h-8 text-teal-400" />
                <div>
                  <h2 className="text-2xl font-bold text-white">Natural Botanical Bio-Pesticide Formulations</h2>
                  <p className="text-xs text-slate-400">Zero synthetic chemical sprays required</p>
                </div>
              </div>

              <div className="space-y-4">
                <div className="p-5 rounded-2xl bg-forest-900/60 border border-forest-800 space-y-2">
                  <h3 className="text-sm font-bold text-emerald-400">1. Cold-Pressed Neem Oil Bio-Spray</h3>
                  <p className="text-xs text-slate-300">
                    <strong>Ingredients:</strong> 5ml cold-pressed pure neem oil + 2ml organic liquid soap + 1 Liter warm water.<br />
                    <strong>Controls:</strong> Aphids, whiteflies, thrips, spider mites, and scale insects.
                  </p>
                </div>

                <div className="p-5 rounded-2xl bg-forest-900/60 border border-forest-800 space-y-2">
                  <h3 className="text-sm font-bold text-amber-300">2. Sour Fermented Buttermilk Spray</h3>
                  <p className="text-xs text-slate-300">
                    <strong>Ingredients:</strong> 100ml 4-day sour fermented buttermilk diluted in 1 Liter fresh water.<br />
                    <strong>Controls:</strong> Fungal powdery mildew, rust, leaf spot, and viral leaf curl diseases.
                  </p>
                </div>

                <div className="p-5 rounded-2xl bg-forest-900/60 border border-forest-800 space-y-2">
                  <h3 className="text-sm font-bold text-rose-300">3. Agniastra Potent Botanical Insecticide</h3>
                  <p className="text-xs text-slate-300">
                    <strong>Ingredients:</strong> Indigenous cow urine, crushed neem leaves, hot green chillies, garlic paste, boiled and filtered.<br />
                    <strong>Controls:</strong> Severe stem borers, pod borers, and destructive fruit flies.
                  </p>
                </div>
              </div>
            </div>
          )}

        </div>
      )}

    </div>
  );
}
