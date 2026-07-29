import React, { useEffect, useState } from 'react';
import { Award, CheckCircle2, XCircle, RotateCcw, ShieldCheck, Sparkles, ArrowRight, HelpCircle } from 'lucide-react';
import { fetchQuizQuestions, submitQuizResult } from '../utils/api';

export default function Quiz() {
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [quizSubmitted, setQuizSubmitted] = useState(false);
  const [result, setResult] = useState(null);
  const [userName, setUserName] = useState('');

  useEffect(() => {
    fetchQuizQuestions().then(setQuestions);
  }, []);

  const handleSelectOption = (optionIndex) => {
    const qid = questions[currentIndex].id;
    setSelectedAnswers({
      ...selectedAnswers,
      [qid]: optionIndex
    });
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  const handleSubmit = async () => {
    const res = await submitQuizResult(selectedAnswers, userName || 'Eco Enthusiast');
    setResult(res);
    setQuizSubmitted(true);
  };

  const handleRestart = () => {
    setSelectedAnswers({});
    setQuizSubmitted(false);
    setResult(null);
    setCurrentIndex(0);
    fetchQuizQuestions().then(setQuestions);
  };

  const currentQ = questions[currentIndex];
  const progressPct = questions.length > 0 ? ((currentIndex + 1) / questions.length) * 100 : 0;

  const getBadgeIconColor = (badge) => {
    switch (badge) {
      case 'Earth Protector': return 'bg-amber-500/20 text-amber-300 border-amber-500/40';
      case 'Green Warrior': return 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40';
      case 'Eco Learner': return 'bg-teal-500/20 text-teal-300 border-teal-500/40';
      default: return 'bg-slate-700/40 text-slate-300 border-slate-600';
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 space-y-8">
      
      {/* Header Banner */}
      <div className="text-center space-y-3">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold uppercase tracking-wider">
          <Award className="w-4 h-4" />
          <span>Dynamic Environmental Knowledge Assessment</span>
        </div>
        <h1 className="text-4xl font-extrabold text-white">Eco Knowledge Quiz</h1>
        <p className="text-slate-300 text-sm max-w-xl mx-auto">
          Test your environmental science and natural farming literacy. Answer questions to unlock environmental badges!
        </p>
      </div>

      {!quizSubmitted ? (
        currentQ ? (
          <div className="bg-forest-950 border border-forest-800/80 rounded-3xl p-6 sm:p-10 space-y-8 shadow-xl">
            
            {/* Progress Bar */}
            <div className="space-y-2">
              <div className="flex justify-between text-xs font-bold text-slate-400">
                <span>Question {currentIndex + 1} of {questions.length}</span>
                <span className="text-emerald-400">{Math.round(progressPct)}% Complete</span>
              </div>
              <div className="w-full bg-forest-900 h-2.5 rounded-full overflow-hidden border border-forest-800">
                <div
                  className="bg-gradient-to-r from-emerald-500 to-forest-500 h-full transition-all duration-300 rounded-full"
                  style={{ width: `${progressPct}%` }}
                ></div>
              </div>
            </div>

            {/* Question Card */}
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-white flex items-start gap-3">
                <HelpCircle className="w-6 h-6 text-emerald-400 shrink-0 mt-0.5" />
                <span>{currentQ.question}</span>
              </h2>

              {/* Options */}
              <div className="space-y-3">
                {currentQ.options.map((opt, idx) => {
                  const isSelected = selectedAnswers[currentQ.id] === idx;
                  return (
                    <button
                      key={idx}
                      onClick={() => handleSelectOption(idx)}
                      className={`w-full text-left p-4 rounded-2xl border transition-all flex items-center justify-between font-medium text-sm ${
                        isSelected
                          ? 'bg-gradient-to-r from-forest-800 to-emerald-900 border-emerald-500 text-white shadow-md'
                          : 'bg-forest-900/60 hover:bg-forest-900 border-forest-800 text-slate-200'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <span className={`w-7 h-7 rounded-full text-xs font-bold flex items-center justify-center border ${
                          isSelected ? 'bg-emerald-500 text-forest-950 border-emerald-400' : 'bg-forest-950 text-slate-400 border-forest-700'
                        }`}>
                          {String.fromCharCode(65 + idx)}
                        </span>
                        <span>{opt}</span>
                      </div>
                      {isSelected && <CheckCircle2 className="w-5 h-5 text-emerald-400" />}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* User Name Input on Last Question */}
            {currentIndex === questions.length - 1 && (
              <div className="p-4 rounded-2xl bg-forest-900/60 border border-forest-800 space-y-2">
                <label className="text-xs font-bold text-emerald-300 block">Your Name (for Badge Certificate):</label>
                <input
                  type="text"
                  value={userName}
                  onChange={(e) => setUserName(e.target.value)}
                  placeholder="Enter your name e.g. Alex Green"
                  className="w-full px-4 py-2.5 rounded-xl bg-forest-950 border border-forest-700 text-white text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
                />
              </div>
            )}

            {/* Navigation Buttons */}
            <div className="flex items-center justify-between pt-4 border-t border-forest-800">
              <button
                onClick={handlePrev}
                disabled={currentIndex === 0}
                className="px-5 py-2.5 rounded-xl bg-forest-900 hover:bg-forest-800 disabled:opacity-30 text-xs font-bold text-slate-300 transition-colors"
              >
                Previous
              </button>

              {currentIndex < questions.length - 1 ? (
                <button
                  onClick={handleNext}
                  disabled={selectedAnswers[currentQ.id] === undefined}
                  className="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 disabled:opacity-40 text-xs font-bold text-white transition-all flex items-center gap-1.5 shadow-md"
                >
                  <span>Next Question</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              ) : (
                <button
                  onClick={handleSubmit}
                  disabled={Object.keys(selectedAnswers).length < questions.length}
                  className="px-8 py-3 rounded-xl bg-gradient-to-r from-emerald-500 to-forest-600 hover:from-emerald-400 hover:to-forest-500 disabled:opacity-40 text-xs font-extrabold text-white transition-all shadow-lg shadow-emerald-500/20"
                >
                  Submit & Get Badge
                </button>
              )}
            </div>

          </div>
        ) : (
          <div className="p-12 text-center text-slate-400">Loading quiz questions...</div>
        )
      ) : (
        /* Results View */
        <div className="bg-forest-950 border border-forest-800/80 rounded-3xl p-8 sm:p-12 space-y-8 shadow-2xl text-center">
          
          <div className="space-y-4">
            <div className="w-20 h-20 rounded-full bg-emerald-500/20 border-2 border-emerald-400 flex items-center justify-center mx-auto text-emerald-400 shadow-xl">
              <Award className="w-10 h-10 animate-pulse" />
            </div>

            <h2 className="text-3xl font-extrabold text-white">Quiz Evaluation Completed!</h2>
            <p className="text-slate-300 text-sm">
              Congratulations <strong className="text-emerald-300">{userName || 'Eco Enthusiast'}</strong>! Here is your assessment summary:
            </p>
          </div>

          {/* Badge Display Box */}
          <div className={`max-w-md mx-auto p-6 rounded-3xl border ${getBadgeIconColor(result?.badge)} space-y-3 shadow-lg`}>
            <span className="text-[11px] uppercase tracking-wider font-extrabold bg-emerald-950/60 px-3 py-1 rounded-full border border-emerald-500/30">
              Badge Unlocked
            </span>
            <h3 className="text-2xl font-black">{result?.badge}</h3>
            <div className="text-3xl font-extrabold text-white">
              {result?.score} / {result?.total} ({result?.percentage}%)
            </div>
          </div>

          {/* All Badges Showcase */}
          <div className="pt-6 border-t border-forest-800 space-y-3">
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Environmental Badge Tiers</h4>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
              <div className={`p-3 rounded-xl border ${result?.badge === 'Eco Beginner' ? 'bg-forest-800 border-emerald-500 text-white font-bold' : 'bg-forest-900/40 border-forest-800 text-slate-400'}`}>
                Eco Beginner (0-39%)
              </div>
              <div className={`p-3 rounded-xl border ${result?.badge === 'Eco Learner' ? 'bg-forest-800 border-emerald-500 text-white font-bold' : 'bg-forest-900/40 border-forest-800 text-slate-400'}`}>
                Eco Learner (40-69%)
              </div>
              <div className={`p-3 rounded-xl border ${result?.badge === 'Green Warrior' ? 'bg-forest-800 border-emerald-500 text-white font-bold' : 'bg-forest-900/40 border-forest-800 text-slate-400'}`}>
                Green Warrior (70-89%)
              </div>
              <div className={`p-3 rounded-xl border ${result?.badge === 'Earth Protector' ? 'bg-forest-800 border-emerald-500 text-white font-bold' : 'bg-forest-900/40 border-forest-800 text-slate-400'}`}>
                Earth Protector (90-100%)
              </div>
            </div>
          </div>

          <button
            onClick={handleRestart}
            className="px-8 py-3.5 rounded-xl bg-forest-800 hover:bg-forest-700 text-white font-bold text-xs transition-colors flex items-center gap-2 mx-auto"
          >
            <RotateCcw className="w-4 h-4 text-emerald-400" />
            <span>Retake Quiz</span>
          </button>

        </div>
      )}

    </div>
  );
}
