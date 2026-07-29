import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Leaf, MessageSquare, BookOpen, Sprout, Award, Calculator, Image, LayoutDashboard, Globe, Menu, X } from 'lucide-react';
import { translations } from '../utils/translations';

export default function Navbar({ language, setLanguage }) {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const t = translations[language] || translations.en;

  const navLinks = [
    { path: '/', label: t.navHome, icon: Leaf },
    { path: '/chat', label: t.navChat, icon: MessageSquare },
    { path: '/learn', label: t.navLearn, icon: BookOpen },
    { path: '/farming', label: t.navFarming, icon: Sprout },
    { path: '/quiz', label: t.navQuiz, icon: Award },
    { path: '/carbon', label: t.navCarbon, icon: Calculator },
    { path: '/poster', label: t.navPoster, icon: Image },
    { path: '/dashboard', label: t.navDashboard, icon: LayoutDashboard },
  ];

  return (
    <header className="sticky top-0 z-50 backdrop-blur-md bg-forest-950/80 border-b border-forest-800/60 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          
          {/* Brand Logo */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="w-11 h-11 rounded-xl bg-gradient-to-tr from-forest-500 to-emerald-400 p-0.5 shadow-md shadow-forest-500/20 group-hover:scale-105 transition-transform duration-300">
              <div className="w-full h-full bg-forest-950 rounded-[10px] flex items-center justify-center">
                <Leaf className="w-6 h-6 text-emerald-400 group-hover:rotate-12 transition-transform duration-300" />
              </div>
            </div>
            <div>
              <span className="text-2xl font-bold font-sans tracking-tight text-white flex items-center gap-1.5">
                EcoGuide <span className="text-emerald-400 font-extrabold">AI</span>
              </span>
              <span className="text-[10px] tracking-widest uppercase text-emerald-300 font-medium block">
                Environmental Mentor
              </span>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center gap-1 bg-forest-900/40 p-1.5 rounded-full border border-forest-800/40">
            {navLinks.map((link) => {
              const Icon = link.icon;
              const isActive = location.pathname === link.path;
              return (
                <Link
                  key={link.path}
                  to={link.path}
                  className={`flex items-center gap-1.5 px-3.5 py-2 rounded-full text-xs font-semibold transition-all duration-200 ${
                    isActive
                      ? 'bg-gradient-to-r from-forest-600 to-emerald-600 text-white shadow-sm shadow-forest-500/30'
                      : 'text-slate-300 hover:text-white hover:bg-forest-800/40'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-emerald-200' : 'text-slate-400'}`} />
                  <span>{link.label}</span>
                </Link>
              );
            })}
          </nav>

          {/* Controls: Language Switch & Mobile Menu Toggle */}
          <div className="flex items-center gap-3">
            <button
              onClick={() => setLanguage(language === 'en' ? 'ta' : 'en')}
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-forest-800/60 border border-forest-700/60 text-emerald-300 hover:bg-forest-700/80 transition-colors"
              title="Toggle English / Tamil"
            >
              <Globe className="w-4 h-4 text-emerald-400" />
              <span>{language === 'en' ? 'English' : 'தமிழ்'}</span>
            </button>

            {/* Mobile menu button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="lg:hidden p-2 rounded-lg bg-forest-900 border border-forest-800 text-slate-300 hover:text-white"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation Drawer */}
      {mobileMenuOpen && (
        <div className="lg:hidden bg-forest-950/95 border-b border-forest-800 px-4 pt-2 pb-4 space-y-2">
          {navLinks.map((link) => {
            const Icon = link.icon;
            const isActive = location.pathname === link.path;
            return (
              <Link
                key={link.path}
                to={link.path}
                onClick={() => setMobileMenuOpen(false)}
                className={`flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive ? 'bg-emerald-600 text-white' : 'text-slate-300 hover:bg-forest-900'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span>{link.label}</span>
              </Link>
            );
          })}
        </div>
      )}
    </header>
  );
}
