import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Trash2, Mic, MicOff, Volume2, VolumeX, Sparkles, CheckCircle2, Lightbulb, Compass, Globe } from 'lucide-react';
import { sendChatMessage } from '../utils/api';
import { translations } from '../utils/translations';

export default function Chat({ language, setLanguage }) {
  const t = translations[language] || translations.en;
  const messagesEndRef = useRef(null);

  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([
    {
      sender: 'ai',
      response: {
        answer: language === 'ta'
          ? "வணக்கம்! நான் EcoGuide AI, உங்கள் இயற்கை மற்றும் சுற்றுச்சூழல் வழிகாட்டி. காலநிலை மாற்றம், இயற்கை விவசாயம் அல்லது கழிவு மேலாண்மை குறித்து ஏதேனும் கேளுங்கள்!"
          : "Hello! I am EcoGuide AI, your intelligent environmental mentor and natural farming assistant. Ask me anything about climate change, water conservation, organic farming, or reducing pollution!",
        tip: "Small daily habits like carrying a reusable water flask make a massive collective impact on ocean plastic reduction.",
        action: "Pick one suggested question below or type your own environmental question to get started!"
      }
    }
  ]);

  // Voice Recognition State
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef(null);

  // Speech Synthesis State
  const [speakingIdx, setSpeakingIdx] = useState(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory, loading]);

  // Initialize SpeechRecognition if browser supports it
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = language === 'ta' ? 'ta-IN' : 'en-US';

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInput(transcript);
        setIsListening(false);
      };

      recognition.onerror = () => setIsListening(false);
      recognition.onend = () => setIsListening(false);

      recognitionRef.current = recognition;
    }
  }, [language]);

  const toggleMic = () => {
    if (!recognitionRef.current) {
      alert("Voice recognition is not supported in this browser. Try Google Chrome or Microsoft Edge.");
      return;
    }
    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      recognitionRef.current.lang = language === 'ta' ? 'ta-IN' : 'en-US';
      recognitionRef.current.start();
      setIsListening(true);
    }
  };

  const handleSpeak = (text, idx) => {
    if (!('speechSynthesis' in window)) return;

    if (speakingIdx === idx) {
      window.speechSynthesis.cancel();
      setSpeakingIdx(null);
      return;
    }

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = language === 'ta' ? 'ta-IN' : 'en-US';
    utterance.rate = 0.95;

    utterance.onend = () => setSpeakingIdx(null);
    utterance.onerror = () => setSpeakingIdx(null);

    setSpeakingIdx(idx);
    window.speechSynthesis.speak(utterance);
  };

  const handleSend = async (customMessage = null) => {
    const queryText = customMessage || input;
    if (!queryText.trim() || loading) return;

    // Append user message
    const newHistory = [
      ...chatHistory,
      { sender: 'user', text: queryText }
    ];
    setChatHistory(newHistory);
    if (!customMessage) setInput('');
    setLoading(true);

    // Call API
    const response = await sendChatMessage(queryText, language);

    setChatHistory([
      ...newHistory,
      { sender: 'ai', response }
    ]);
    setLoading(false);
  };

  const clearChat = () => {
    if (window.speechSynthesis) window.speechSynthesis.cancel();
    setSpeakingIdx(null);
    setChatHistory([
      {
        sender: 'ai',
        response: {
          answer: language === 'ta'
            ? "வரலாறு அழிக்கப்பட்டது. புதிய கேள்வியைக் கேளுங்கள்!"
            : "Chat history cleared. What would you like to explore next?",
          tip: "Composting organic waste builds fertile living soil.",
          action: "Select a topic card or ask a new question."
        }
      }
    ]);
  };

  const suggestedQuestions = [
    "What is climate change?",
    "How can I save water?",
    "Explain natural farming.",
    "How can I reduce pollution?",
    "What is biodiversity?"
  ];

  return (
    <div className="max-w-5xl mx-auto py-8 px-4 sm:px-6 space-y-6">
      
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 p-4 rounded-2xl bg-forest-900/60 border border-forest-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex items-center justify-center shadow-md">
            <Bot className="w-6 h-6 text-forest-950" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-white flex items-center gap-2">
              EcoGuide AI Conversational Mentor
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                Groq RAG
              </span>
            </h1>
            <p className="text-xs text-slate-400">Ask questions in simple beginner-friendly language</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {/* Language Switch */}
          <button
            onClick={() => setLanguage(language === 'en' ? 'ta' : 'en')}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-forest-800 border border-forest-700 text-xs font-semibold text-emerald-300 hover:bg-forest-700 transition-colors"
          >
            <Globe className="w-4 h-4" />
            <span>{language === 'en' ? 'English' : 'தமிழ்'}</span>
          </button>

          {/* Clear History */}
          <button
            onClick={clearChat}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-300 hover:bg-rose-500/20 text-xs font-semibold transition-colors"
            title="Clear Chat History"
          >
            <Trash2 className="w-4 h-4" />
            <span>{t.clearChat}</span>
          </button>
        </div>
      </div>

      {/* Suggested Questions */}
      <div className="space-y-2">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1">
          <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
          {t.suggestedQuestions}:
        </span>
        <div className="flex flex-wrap gap-2">
          {suggestedQuestions.map((q, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(q)}
              className="text-xs px-3.5 py-2 rounded-xl bg-forest-900/80 hover:bg-forest-800 border border-forest-700/80 text-emerald-300 hover:text-white transition-all transform hover:-translate-y-0.5"
            >
              {q}
            </button>
          ))}
        </div>
      </div>

      {/* Chat Messages Box */}
      <div className="bg-forest-950/80 border border-forest-800/80 rounded-3xl p-6 min-h-[480px] max-h-[600px] overflow-y-auto space-y-6 shadow-inner">
        {chatHistory.map((item, idx) => (
          <div key={idx} className={`flex gap-3 ${item.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            
            {item.sender === 'ai' && (
              <div className="w-8 h-8 rounded-lg bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400 shrink-0 mt-1">
                <Bot className="w-5 h-5" />
              </div>
            )}

            <div className={`max-w-2xl rounded-2xl p-5 space-y-4 shadow-md ${
              item.sender === 'user'
                ? 'bg-gradient-to-r from-forest-700 to-emerald-700 text-white rounded-tr-none'
                : 'bg-forest-900/90 border border-forest-800 text-slate-100 rounded-tl-none'
            }`}>
              {item.sender === 'user' ? (
                <p className="text-sm font-medium leading-relaxed">{item.text}</p>
              ) : (
                <div className="space-y-4 text-xs sm:text-sm">
                  
                  {/* Answer Section */}
                  <div className="space-y-1">
                    <span className="text-[11px] uppercase tracking-wider font-bold text-emerald-400 flex items-center gap-1.5">
                      <Bot className="w-3.5 h-3.5" />
                      {t.answerTitle}
                    </span>
                    <p className="text-slate-200 leading-relaxed font-sans text-sm">
                      {item.response.answer}
                    </p>
                  </div>

                  {/* Environmental Tip Section */}
                  {item.response.tip && (
                    <div className="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-200 space-y-1">
                      <span className="text-[11px] uppercase tracking-wider font-bold text-amber-300 flex items-center gap-1.5">
                        <Lightbulb className="w-3.5 h-3.5 text-amber-300" />
                        {t.tipTitle}
                      </span>
                      <p className="text-xs text-amber-100">{item.response.tip}</p>
                    </div>
                  )}

                  {/* Action User Can Take Section */}
                  {item.response.action && (
                    <div className="p-3.5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-200 space-y-1">
                      <span className="text-[11px] uppercase tracking-wider font-bold text-emerald-300 flex items-center gap-1.5">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-300" />
                        {t.actionTitle}
                      </span>
                      <p className="text-xs text-emerald-100">{item.response.action}</p>
                    </div>
                  )}

                  {/* Text-To-Speech Button */}
                  <div className="pt-2 flex justify-end">
                    <button
                      onClick={() => handleSpeak(`${item.response.answer}. Tip: ${item.response.tip}. Action: ${item.response.action}`, idx)}
                      className="flex items-center gap-1 px-2.5 py-1 rounded-md bg-forest-800 hover:bg-forest-700 text-xs font-medium text-slate-300 hover:text-white transition-colors"
                      title="Audio Speech Synthesis"
                    >
                      {speakingIdx === idx ? (
                        <>
                          <VolumeX className="w-3.5 h-3.5 text-rose-400 animate-pulse" />
                          <span className="text-rose-400">{t.stopSpeak}</span>
                        </>
                      ) : (
                        <>
                          <Volume2 className="w-3.5 h-3.5 text-emerald-400" />
                          <span>{t.speakResponse}</span>
                        </>
                      )}
                    </button>
                  </div>
                </div>
              )}
            </div>

            {item.sender === 'user' && (
              <div className="w-8 h-8 rounded-lg bg-forest-700 border border-forest-600 flex items-center justify-center text-slate-200 shrink-0 mt-1">
                <User className="w-5 h-5" />
              </div>
            )}
          </div>
        ))}

        {/* Typing Animation Indicator */}
        {loading && (
          <div className="flex gap-3 items-center text-slate-400 text-xs italic bg-forest-900/50 p-4 rounded-2xl border border-forest-800 max-w-sm">
            <Bot className="w-5 h-5 text-emerald-400 animate-bounce" />
            <span>EcoGuide AI is researching knowledge base and synthesizing answer...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Form with Speech-to-Text */}
      <form onSubmit={(e) => { e.preventDefault(); handleSend(); }} className="flex items-center gap-3">
        <div className="relative flex-1">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={isListening ? t.micListening : t.placeholderChat}
            className={`w-full px-5 py-4 rounded-2xl bg-forest-900/90 border text-white placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 shadow-lg ${
              isListening ? 'border-emerald-400 ring-2 ring-emerald-500/50 animate-pulse' : 'border-forest-700'
            }`}
          />

          <button
            type="button"
            onClick={toggleMic}
            className={`absolute right-3 top-1/2 -translate-y-1/2 p-2 rounded-xl text-xs font-semibold transition-all ${
              isListening
                ? 'bg-rose-500 text-white animate-pulse'
                : 'bg-forest-800 hover:bg-forest-700 text-emerald-300'
            }`}
            title="Speech-to-Text Input"
          >
            {isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
          </button>
        </div>

        <button
          type="submit"
          disabled={!input.trim() || loading}
          className="px-6 py-4 rounded-2xl bg-gradient-to-r from-emerald-500 to-forest-600 hover:from-emerald-400 hover:to-forest-500 text-white font-bold disabled:opacity-50 transition-all flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/20"
        >
          <span>{t.send}</span>
          <Send className="w-4 h-4" />
        </button>
      </form>

    </div>
  );
}
