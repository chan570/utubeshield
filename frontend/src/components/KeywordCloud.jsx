import React from 'react';
import { Tag, Lightbulb, AlertTriangle } from 'lucide-react';

export default function KeywordCloud({ analytics }) {
  if (!analytics) return null;

  const keywords = analytics.top_keywords || [];
  const complaints = analytics.common_complaints || [];
  const requests = analytics.requested_features || [];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
      {/* Top Keywords */}
      <div className="glass-panel rounded-2xl p-5 border-2 border-peach-200 bg-white shadow-sm">
        <div className="flex items-center gap-2 text-xs font-black text-peach-950 uppercase tracking-wider mb-3">
          <Tag className="w-4 h-4 text-peach-700" />
          <span>Top Mentioned Keywords</span>
        </div>

        <div className="flex flex-wrap gap-2">
          {keywords.length > 0 ? (
            keywords.map((kw, i) => (
              <span
                key={i}
                className="px-3.5 py-1.5 rounded-lg bg-peach-100 border-2 border-peach-300 text-peach-950 text-xs font-extrabold flex items-center gap-1.5 shadow-sm"
              >
                <span>#{kw.keyword}</span>
                <span className="px-2 py-0.5 rounded bg-peach-300 text-[11px] font-black text-peach-950">
                  {kw.count}
                </span>
              </span>
            ))
          ) : (
            <p className="text-xs text-gray-800 font-bold">No keyword clusters detected.</p>
          )}
        </div>
      </div>

      {/* Most Requested Features */}
      <div className="glass-panel rounded-2xl p-5 border-2 border-peach-200 bg-white shadow-sm">
        <div className="flex items-center gap-2 text-xs font-black text-emerald-950 uppercase tracking-wider mb-3">
          <Lightbulb className="w-4 h-4 text-emerald-700" />
          <span>Requested Video Topics & Features</span>
        </div>

        <div className="space-y-2">
          {requests.length > 0 ? (
            requests.slice(0, 3).map((req, i) => (
              <div key={i} className="p-3 rounded-xl bg-emerald-100/70 border border-emerald-300 text-xs text-emerald-950 font-extrabold line-clamp-2 shadow-sm">
                "{req}"
              </div>
            ))
          ) : (
            <p className="text-xs text-gray-800 font-bold">No feature requests recorded.</p>
          )}
        </div>
      </div>

      {/* Common Complaints */}
      <div className="glass-panel rounded-2xl p-5 border-2 border-peach-200 bg-white shadow-sm">
        <div className="flex items-center gap-2 text-xs font-black text-amber-950 uppercase tracking-wider mb-3">
          <AlertTriangle className="w-4 h-4 text-amber-700" />
          <span>Common Viewer Complaints</span>
        </div>

        <div className="space-y-2">
          {complaints.length > 0 ? (
            complaints.slice(0, 3).map((comp, i) => (
              <div key={i} className="p-3 rounded-xl bg-amber-100/70 border border-amber-300 text-xs text-amber-950 font-extrabold line-clamp-2 shadow-sm">
                "{comp}"
              </div>
            ))
          ) : (
            <p className="text-xs text-gray-800 font-bold">No major complaints detected.</p>
          )}
        </div>
      </div>
    </div>
  );
}
