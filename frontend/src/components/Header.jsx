import React, { useEffect, useState } from 'react';
import { ShieldCheck, Activity, Cpu } from 'lucide-react';
import { getHealth } from '../services/api';

export default function Header() {
  const [systemHealth, setSystemHealth] = useState(null);

  useEffect(() => {
    getHealth()
      .then(data => setSystemHealth(data))
      .catch(() => setSystemHealth({ mock_mode: true, status: 'offline' }));
  }, []);

  return (
    <header className="glass-panel sticky top-0 z-40 border-b border-peach-200 px-6 py-4 mb-8 bg-white/95 shadow-sm">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
        {/* Brand & Logo */}
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-peach-600 via-rose-500 to-amber-500 flex items-center justify-center shadow-md shadow-peach-600/30">
            <ShieldCheck className="w-6 h-6 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-black tracking-tight text-[#1a0f0b]">TubeShield AI</h1>
              <span className="text-[10px] uppercase tracking-wider font-extrabold px-2.5 py-0.5 rounded-full bg-peach-100 text-peach-900 border border-peach-300">
                LangGraph Multi-Agent
              </span>
            </div>
            <p className="text-xs text-gray-700 font-semibold">Autonomous YouTube Comment Moderation & Community Intelligence</p>
          </div>
        </div>

        {/* System Status Indicators */}
        <div className="flex items-center gap-3 text-xs font-bold">
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-peach-100/80 border border-peach-300 text-gray-900 shadow-sm">
            <Cpu className="w-4 h-4 text-peach-700" />
            <span>LLM: <strong className="text-peach-900 font-black">OpenAI / Gemini</strong></span>
          </div>

          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-100/80 border border-emerald-300 text-gray-900 shadow-sm">
            <Activity className="w-4 h-4 text-emerald-700" />
            <span>Mode: <strong className={systemHealth?.mock_mode ? "text-amber-900" : "text-emerald-900"}>
              {systemHealth?.mock_mode ? "Active Engine" : "Live API Connected"}
            </strong></span>
          </div>
        </div>
      </div>
    </header>
  );
}
