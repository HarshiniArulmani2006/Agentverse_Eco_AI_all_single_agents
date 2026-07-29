import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import DailyTipModal from './components/DailyTipModal';
import Home from './pages/Home';
import Chat from './pages/Chat';
import Learn from './pages/Learn';
import NaturalFarming from './pages/NaturalFarming';
import Quiz from './pages/Quiz';
import CarbonCalculator from './pages/CarbonCalculator';
import PosterGenerator from './pages/PosterGenerator';
import Dashboard from './pages/Dashboard';

export default function App() {
  const [language, setLanguage] = useState('en'); // 'en' or 'ta'

  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-forest-950 text-slate-100 font-sans selection:bg-emerald-500 selection:text-forest-950">
        
        {/* Daily Eco Tip Notification Banner */}
        <DailyTipModal />

        {/* Global Navigation Header */}
        <Navbar language={language} setLanguage={setLanguage} />

        {/* Main Route Body */}
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home language={language} />} />
            <Route path="/chat" element={<Chat language={language} setLanguage={setLanguage} />} />
            <Route path="/learn" element={<Learn language={language} />} />
            <Route path="/farming" element={<NaturalFarming language={language} />} />
            <Route path="/quiz" element={<Quiz language={language} />} />
            <Route path="/carbon" element={<CarbonCalculator language={language} />} />
            <Route path="/poster" element={<PosterGenerator language={language} />} />
            <Route path="/dashboard" element={<Dashboard language={language} />} />
          </Routes>
        </main>

        {/* Global Footer */}
        <Footer />

      </div>
    </Router>
  );
}
