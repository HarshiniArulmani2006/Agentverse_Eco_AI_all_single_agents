import React, { useState, useRef } from 'react';
import { Image, Sparkles, Download, Printer, RefreshCw, Leaf, ShieldAlert, Layers } from 'lucide-react';
import { generateAwarenessPoster } from '../utils/api';

export default function PosterGenerator() {
  const [category, setCategory] = useState('climate');
  const [customTitle, setCustomTitle] = useState('');
  const [theme, setTheme] = useState('emerald-forest');
  const [layoutStyle, setLayoutStyle] = useState('centered');
  
  const [poster, setPoster] = useState({
    title: "Protect Earth: Climate Action",
    slogan: "Small Steps Today, A Greener Tomorrow",
    category: "climate",
    layoutStyle: "centered",
    theme: {
      id: "emerald-forest",
      name: "Emerald Forest",
      primaryColor: "#1b4332",
      accentColor: "#52b788",
      bgGradient: "from-emerald-950 via-forest-900 to-green-950",
      textColor: "#ffffff"
    },
    tip: "Share this poster to inspire eco-friendly daily habits in your school, office, or community!",
    callToAction: "Join the EcoGuide AI Green Movement Today"
  });

  const [loading, setLoading] = useState(false);
  const posterRef = useRef(null);

  const handleGenerate = async (e) => {
    if (e) e.preventDefault();
    setLoading(true);
    const res = await generateAwarenessPoster({ category, customTitle, theme, layoutStyle });
    setPoster(res);
    setLoading(false);
  };

  // High-Resolution HTML5 Canvas PNG Generator & File Downloader
  const handleDownload = () => {
    const canvas = document.createElement('canvas');
    const width = 1200;
    const height = 1600;
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');

    // Color mappings based on theme
    const themeColors = {
      'emerald-forest': { bg1: '#022c22', bg2: '#064e3b', accent: '#34d399', text: '#ffffff' },
      'ocean-blue': { bg1: '#0284c7', bg2: '#0c4a6e', accent: '#38bdf8', text: '#ffffff' },
      'earth-harvest': { bg1: '#451a03', bg2: '#78350f', accent: '#fde047', text: '#ffffff' },
      'solar-glow': { bg1: '#7c2d12', bg2: '#9a3412', accent: '#fbbf24', text: '#ffffff' },
      'botanical-bloom': { bg1: '#064e3b', bg2: '#115e59', accent: '#6ee7b7', text: '#ffffff' },
      'neon-eco': { bg1: '#000000', bg2: '#022c22', accent: '#00ff87', text: '#00ff87' },
      'midnight-canopy': { bg1: '#2e1065', bg2: '#3b0764', accent: '#c084fc', text: '#ffffff' },
      'sunset-radiance': { bg1: '#881337', bg2: '#701a75', accent: '#fda4af', text: '#ffffff' }
    };

    const palette = themeColors[poster.theme?.id || theme] || themeColors['emerald-forest'];

    // 1. Draw Background Gradient
    const gradient = ctx.createLinearGradient(0, 0, 0, height);
    gradient.addColorStop(0, palette.bg1);
    gradient.addColorStop(0.5, palette.bg2);
    gradient.addColorStop(1, '#000000');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, width, height);

    // 2. Draw Decorative Top Bar & Border
    ctx.strokeStyle = palette.accent;
    ctx.lineWidth = 16;
    ctx.strokeRect(30, 30, width - 60, height - 60);

    ctx.fillStyle = palette.accent;
    ctx.fillRect(30, 30, width - 60, 24);

    // 3. Draw Header Tag
    ctx.fillStyle = 'rgba(255, 255, 255, 0.15)';
    ctx.beginPath();
    ctx.roundRect(width / 2 - 250, 120, 500, 60, 30);
    ctx.fill();

    ctx.fillStyle = palette.accent;
    ctx.font = 'bold 24px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('ECO AWARENESS CAMPAIGN', width / 2, 158);

    // 4. Draw Main Title (Wrapped)
    ctx.fillStyle = palette.text;
    ctx.font = 'black 64px sans-serif';
    ctx.textAlign = 'center';

    const words = poster.title.toUpperCase().split(' ');
    let line = '';
    let y = 340;
    for (let i = 0; i < words.length; i++) {
      let testLine = line + words[i] + ' ';
      let metrics = ctx.measureText(testLine);
      if (metrics.width > width - 200 && i > 0) {
        ctx.fillText(line, width / 2, y);
        line = words[i] + ' ';
        y += 80;
      } else {
        line = testLine;
      }
    }
    ctx.fillText(line, width / 2, y);

    // 5. Draw Slogan Quote Box
    const boxY = y + 80;
    ctx.fillStyle = 'rgba(0, 0, 0, 0.4)';
    ctx.beginPath();
    ctx.roundRect(100, boxY, width - 200, 360, 32);
    ctx.fill();
    ctx.strokeStyle = palette.accent;
    ctx.lineWidth = 4;
    ctx.stroke();

    ctx.fillStyle = palette.accent;
    ctx.font = 'italic bold 44px Georgia, serif';
    const sloganWords = (`"${poster.slogan}"`).split(' ');
    let sloganLine = '';
    let sloganY = boxY + 120;
    for (let i = 0; i < sloganWords.length; i++) {
      let testLine = sloganLine + sloganWords[i] + ' ';
      let metrics = ctx.measureText(testLine);
      if (metrics.width > width - 280 && i > 0) {
        ctx.fillText(sloganLine, width / 2, sloganY);
        sloganLine = sloganWords[i] + ' ';
        sloganY += 60;
      } else {
        sloganLine = testLine;
      }
    }
    ctx.fillText(sloganLine, width / 2, sloganY);

    // 6. Draw Call To Action & Footer
    ctx.fillStyle = palette.accent;
    ctx.font = 'bold 36px sans-serif';
    ctx.fillText(poster.callToAction, width / 2, height - 200);

    ctx.fillStyle = '#94a3b8';
    ctx.font = '22px sans-serif';
    ctx.fillText('EcoGuide AI Platform • www.ecoguideai.org', width / 2, height - 120);

    // 7. Trigger PNG Download
    const dataUrl = canvas.toDataURL('image/png');
    const link = document.createElement('a');
    link.download = `Eco_Awareness_Poster_${category}.png`;
    link.href = dataUrl;
    link.click();
  };

  // Browser Print Trigger
  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="max-w-6xl mx-auto py-8 px-4 sm:px-6 space-y-10">
      
      {/* Header */}
      <div className="text-center space-y-3">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold uppercase tracking-wider">
          <Image className="w-4 h-4" />
          <span>AI Environmental Campaign Creator</span>
        </div>
        <h1 className="text-4xl font-extrabold text-white">Awareness Poster Generator</h1>
        <p className="text-slate-300 text-sm max-w-xl mx-auto">
          Generate impactful, high-aesthetic environmental posters with customizable themes, layouts, and direct high-resolution PNG download and print support.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 print:block">
        
        {/* Controls Column (Hidden during printing) */}
        <div className="lg:col-span-5 bg-forest-950 border border-forest-800 rounded-3xl p-6 space-y-6 shadow-xl print:hidden">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-emerald-400" />
            <span>Design Parameters</span>
          </h2>

          <form onSubmit={handleGenerate} className="space-y-4 text-xs">
            
            <div className="space-y-1.5">
              <label className="font-bold text-slate-300">Campaign Category:</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl bg-forest-900 border border-forest-700 text-white font-medium"
              >
                <option value="climate">Climate Change & Global Warming</option>
                <option value="pollution">Air & Ocean Plastic Pollution</option>
                <option value="farming">Organic & Natural Farming</option>
                <option value="biodiversity">Wildlife & Biodiversity Loss</option>
              </select>
            </div>

            <div className="space-y-1.5">
              <label className="font-bold text-slate-300">Custom Title / Slogan (Optional):</label>
              <input
                type="text"
                value={customTitle}
                onChange={(e) => setCustomTitle(e.target.value)}
                placeholder="e.g. Save Trees, Save Future"
                className="w-full px-4 py-2.5 rounded-xl bg-forest-900 border border-forest-700 text-white"
              />
            </div>

            <div className="space-y-1.5">
              <label className="font-bold text-slate-300">Visual Theme (8 Styles):</label>
              <select
                value={theme}
                onChange={(e) => setTheme(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl bg-forest-900 border border-forest-700 text-white font-medium"
              >
                <option value="emerald-forest">Emerald Forest Green</option>
                <option value="ocean-blue">Ocean Cleanse Blue</option>
                <option value="earth-harvest">Warm Earth Tone</option>
                <option value="solar-glow">Solar Dawn Amber</option>
                <option value="botanical-bloom">Botanical Garden Emerald</option>
                <option value="neon-eco">Cyber Green High-Contrast</option>
                <option value="midnight-canopy">Midnight Forest Purple</option>
                <option value="sunset-radiance">Sunset Eco Rose</option>
              </select>
            </div>

            <div className="space-y-1.5">
              <label className="font-bold text-slate-300 flex items-center gap-1.5">
                <Layers className="w-3.5 h-3.5 text-emerald-400" /> Layout Template Style:
              </label>
              <select
                value={layoutStyle}
                onChange={(e) => setLayoutStyle(e.target.value)}
                className="w-full px-4 py-2.5 rounded-xl bg-forest-900 border border-forest-700 text-white font-medium"
              >
                <option value="centered">Classic Centered Badge</option>
                <option value="hero">Bold Hero Headline</option>
                <option value="quote">Featured Graphic Quote</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3.5 rounded-xl bg-gradient-to-r from-emerald-500 to-forest-600 hover:from-emerald-400 hover:to-forest-500 text-white font-bold shadow-lg shadow-emerald-500/20 transition-all flex items-center justify-center gap-2"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              <span>{loading ? 'Designing Poster...' : 'Generate New Poster'}</span>
            </button>
          </form>
        </div>

        {/* Poster Canvas Preview Column */}
        <div className="lg:col-span-7 space-y-4">
          
          <div className="flex justify-between items-center px-2 print:hidden">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Live Poster Preview</span>
            <div className="flex items-center gap-2">
              <button
                onClick={handleDownload}
                className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition-all shadow-md active:scale-95"
              >
                <Download className="w-4 h-4" />
                <span>Save HD PNG</span>
              </button>
              <button
                onClick={handlePrint}
                className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-forest-800 hover:bg-forest-700 border border-forest-700 text-white text-xs font-bold transition-all shadow-md active:scale-95"
              >
                <Printer className="w-4 h-4 text-emerald-400" />
                <span>Print Poster</span>
              </button>
            </div>
          </div>

          {/* Render Visual Poster */}
          <div
            ref={posterRef}
            className={`rounded-3xl border-4 border-emerald-500/40 p-8 sm:p-12 text-center space-y-8 shadow-2xl relative overflow-hidden bg-gradient-to-b ${poster.theme?.bgGradient || 'from-forest-950 via-forest-900 to-emerald-950'}`}
          >
            <div className="absolute top-0 left-0 w-full h-3 bg-gradient-to-r from-emerald-400 via-teal-400 to-emerald-500"></div>

            <div className="w-16 h-16 rounded-2xl bg-emerald-500/20 border border-emerald-400/40 flex items-center justify-center mx-auto text-emerald-400 shadow-xl">
              <Leaf className="w-8 h-8" />
            </div>

            <div className="space-y-3">
              <span className="text-xs font-bold uppercase tracking-widest text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/30">
                Eco Awareness Campaign
              </span>
              <h2 className="text-3xl sm:text-4xl font-black text-white leading-tight uppercase tracking-tight">
                {poster.title}
              </h2>
            </div>

            <div className="p-6 rounded-2xl bg-forest-900/60 border border-emerald-500/30 text-amber-200 font-extrabold text-xl sm:text-2xl italic leading-snug shadow-inner">
              "{poster.slogan}"
            </div>

            <div className="pt-4 space-y-2 border-t border-forest-800 text-xs text-slate-300">
              <p className="text-emerald-300 font-bold">{poster.callToAction}</p>
              <span className="text-[10px] text-slate-400 block">EcoGuide AI Platform • www.ecoguideai.org</span>
            </div>
          </div>

        </div>

      </div>

    </div>
  );
}
