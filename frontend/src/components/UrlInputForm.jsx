import React, { useState } from 'react';
import { Youtube, Loader2, Sparkles, AlertCircle, ArrowRight } from 'lucide-react';

export default function UrlInputForm({ onAnalyze, isLoading }) {
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');

  const sampleUrls = [
    { label: '🔥 LangGraph AI Tutorial (Recommended Demo)', url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' }
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!url.trim()) {
      setError('Please paste a valid YouTube video URL or ID.');
      return;
    }
    setError('');
    onAnalyze(url.trim());
  };

  const handleSelectSample = (sampleUrl) => {
    setUrl(sampleUrl);
    setError('');
    onAnalyze(sampleUrl);
  };

  return (
    <div className="glass-panel rounded-2xl p-6 mb-8 relative overflow-hidden bg-white border-2 border-peach-200 glow-peach shadow-md">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-6">
          <h2 className="text-2xl sm:text-3xl font-black text-[#1a0f0b] mb-2 flex items-center justify-center gap-2">
            Analyze YouTube Video Comments <Sparkles className="w-6 h-6 text-peach-600 animate-pulse" />
          </h2>
          <p className="text-sm text-gray-800 font-semibold">
            Paste any YouTube video link below to trigger the 7-Agent LangGraph moderation & analytics engine.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="relative mb-4">
          <div className="relative flex items-center">
            <div className="absolute left-4 text-red-600 pointer-events-none">
              <Youtube className="w-6 h-6" />
            </div>
            
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Paste YouTube Video URL (e.g., https://www.youtube.com/watch?v=...)"
              disabled={isLoading}
              className="w-full bg-white border-2 border-peach-300 rounded-xl py-4 pl-12 pr-36 text-sm text-[#1a0f0b] placeholder-gray-500 focus:outline-none focus:border-peach-600 focus:ring-2 focus:ring-peach-500/30 font-bold shadow-inner"
            />

            <button
              type="submit"
              disabled={isLoading}
              className="absolute right-2 top-2 bottom-2 px-6 bg-[#e64a19] hover:bg-[#d84315] text-white font-black rounded-lg text-sm flex items-center gap-2 transition-all shadow-md shadow-orange-600/40 disabled:opacity-50 cursor-pointer z-10"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin text-white" />
                  <span className="text-white font-black">Analyzing...</span>
                </>
              ) : (
                <>
                  <span className="text-white font-black text-sm">Analyze</span>
                  <ArrowRight className="w-4 h-4 text-white" />
                </>
              )}
            </button>
          </div>
        </form>

        {error && (
          <div className="flex items-center gap-2 text-rose-700 font-bold text-xs mt-2 justify-center">
            <AlertCircle className="w-4 h-4" />
            <span>{error}</span>
          </div>
        )}

        {/* Quick Sample Selector */}
        <div className="flex flex-wrap items-center justify-center gap-2 mt-4 text-xs font-bold text-gray-800">
          <span className="font-black text-[#1a0f0b]">Quick Test:</span>
          {sampleUrls.map((s, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleSelectSample(s.url)}
              disabled={isLoading}
              className="px-3.5 py-2 rounded-lg bg-peach-100 hover:bg-peach-200 border-2 border-peach-300 text-peach-950 transition-all text-xs flex items-center gap-1 font-extrabold shadow-sm"
            >
              {s.label}
            </button>
          ))}
        </div>

        {/* Animated Progress Indicator when Loading */}
        {isLoading && (
          <div className="mt-6 p-4 rounded-xl bg-peach-100/90 border-2 border-peach-300 text-center animate-pulse shadow-sm">
            <div className="flex items-center justify-center gap-3 text-peach-950 text-sm font-black mb-2">
              <Loader2 className="w-5 h-5 animate-spin text-peach-700" />
              <span>Executing LangGraph Multi-Agent Pipeline...</span>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-[11px] text-gray-900 mt-3 font-extrabold">
              <div className="p-2.5 rounded bg-white border border-peach-300 shadow-sm">1. Fetching Comments</div>
              <div className="p-2.5 rounded bg-white border border-peach-300 shadow-sm">2. Spam & Toxicity Check</div>
              <div className="p-2.5 rounded bg-white border border-peach-300 shadow-sm">3. Sentiment & Decision Matrix</div>
              <div className="p-2.5 rounded bg-white border border-peach-300 shadow-sm">4. Community Health Scoring</div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
