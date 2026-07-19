import React from 'react';
import { CheckCircle } from 'lucide-react';

export default function HealthScoreMeter({ analytics }) {
  if (!analytics) return null;

  const score = analytics.health_score ?? 85;

  const getScoreBadge = (val) => {
    if (val >= 80) return { label: 'Optimal Health', color: 'text-emerald-950', bg: 'bg-emerald-200 border-emerald-400', stroke: '#059669' };
    if (val >= 60) return { label: 'Moderate Health', color: 'text-amber-950', bg: 'bg-amber-200 border-amber-400', stroke: '#d97706' };
    return { label: 'Needs Attention', color: 'text-rose-950', bg: 'bg-rose-200 border-rose-400', stroke: '#e11d48' };
  };

  const badge = getScoreBadge(score);

  return (
    <div className="glass-panel rounded-2xl p-6 mb-8 border-2 border-peach-200 bg-white glow-peach shadow-md">
      <div className="flex flex-col lg:flex-row items-center justify-between gap-6">

        {/* Score Radial Visual */}
        <div className="flex items-center gap-6 flex-shrink-0">
          <div className="relative w-32 h-32 flex items-center justify-center">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
              <path
                className="text-peach-100"
                strokeWidth="4"
                stroke="currentColor"
                fill="none"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
              <path
                strokeWidth="4"
                strokeDasharray={`${score}, 100`}
                strokeLinecap="round"
                stroke={badge.stroke}
                fill="none"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
            </svg>
            <div className="absolute flex flex-col items-center justify-center text-center">
              <span className="text-4xl font-black text-[#1a0f0b]">{score}</span>
              <span className="text-[11px] text-gray-800 font-extrabold uppercase">/ 100</span>
            </div>
          </div>

          <div>
            <div className="flex items-center gap-2 mb-1.5">
              <span className={`text-xs font-black px-3 py-1 rounded-full border-2 ${badge.bg} ${badge.color}`}>
                {badge.label}
              </span>
            </div>
            <h3 className="text-2xl font-black text-[#1a0f0b] mb-1">Community Health Score</h3>
            <p className="text-xs text-gray-800 max-w-sm leading-relaxed font-bold">
              {analytics.health_reason || "Calculated using real-time toxicity, spam ratio, and viewer sentiment vectors."}
            </p>
          </div>
        </div>

        {/* AI Actionable Recommendations */}
        <div className="flex-1 w-full bg-peach-100/70 rounded-xl p-4 border-2 border-peach-300 shadow-sm">
          <div className="flex items-center gap-2 text-xs font-black text-peach-950 uppercase tracking-wider mb-2.5">
            <CheckCircle className="w-4 h-4 text-peach-700" />
            <span>AI Moderation Recommendations</span>
          </div>

          <ul className="space-y-2 text-xs text-[#1a0f0b] font-bold">
            {analytics.recommendations && analytics.recommendations.length > 0 ? (
              analytics.recommendations.map((rec, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="w-2 h-2 rounded-full bg-peach-600 mt-1 flex-shrink-0" />
                  <span>{rec}</span>
                </li>
              ))
            ) : (
              <li className="text-gray-800 font-bold">All community health parameters are performing well.</li>
            )}
          </ul>
        </div>

      </div>
    </div>
  );
}
