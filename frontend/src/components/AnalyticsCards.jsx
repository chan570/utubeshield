import React from 'react';
import { MessageSquare, ThumbsUp, ThumbsDown, ShieldAlert } from 'lucide-react';

export default function AnalyticsCards({ analytics, commentsCount }) {
  if (!analytics) return null;

  const cards = [
    {
      label: 'Total Analyzed',
      value: analytics.total_comments || commentsCount || 0,
      subtext: 'Comments parsed by LangGraph',
      icon: MessageSquare,
      color: 'from-peach-600 to-rose-500',
    },
    {
      label: 'Positive Sentiment',
      value: `${analytics.positive_pct}%`,
      subtext: 'Compliments & praise',
      icon: ThumbsUp,
      color: 'from-emerald-600 to-teal-500',
    },
    {
      label: 'Negative Sentiment',
      value: `${analytics.negative_pct}%`,
      subtext: 'Complaints & criticisms',
      icon: ThumbsDown,
      color: 'from-amber-600 to-orange-500',
    },
    {
      label: 'Spam Detected',
      value: `${analytics.spam_pct}%`,
      subtext: 'Crypto, bots & scam links',
      icon: ShieldAlert,
      color: 'from-rose-600 to-red-600',
    }
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
      {cards.map((card, idx) => {
        const IconComponent = card.icon;
        return (
          <div key={idx} className="glass-panel rounded-2xl p-5 border-2 border-peach-200 bg-white flex items-center justify-between group hover:border-peach-400 transition-all shadow-sm">
            <div>
              <p className="text-xs text-gray-800 uppercase font-black tracking-wider mb-1">{card.label}</p>
              <h4 className="text-3xl font-black text-[#1a0f0b] mb-1">{card.value}</h4>
              <p className="text-xs text-gray-700 font-bold">{card.subtext}</p>
            </div>
            <div className={`w-12 h-12 rounded-xl bg-gradient-to-tr ${card.color} flex items-center justify-center shadow-md group-hover:scale-110 transition-transform`}>
              <IconComponent className="w-6 h-6 text-white" />
            </div>
          </div>
        );
      })}
    </div>
  );
}
