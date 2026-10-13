import React from 'react';
import { Orbit, ShieldCheck, Cpu, Database } from 'lucide-react';
import { useMode } from '../../context/ModeContext';

export const Footer: React.FC = () => {
  const { mode } = useMode();

  return (
    <footer className="glass-panel border-t border-white/10 mt-20 py-8 px-4 lg:px-8 text-xs text-slate-400">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="flex items-center space-x-3">
          <Orbit className="w-5 h-5 text-sky-400" />
          <div>
            <p className="font-semibold text-slate-200">
              NEBULA: Intelligent Astronomical Data Platform
            </p>
            <p className="text-[11px] text-slate-400">
              Research-oriented BTech CSE Capstone Project • Unified Astronomical Data Foundation
            </p>
          </div>
        </div>

        {/* Real-time system provenance badges */}
        <div className="flex flex-wrap items-center gap-2 text-[11px]">
          <span className="flex items-center space-x-1 px-2.5 py-1 rounded-md bg-white/5 border border-white/10 text-slate-300">
            <Database className="w-3 h-3 text-sky-400" />
            <span>NASA / JPL / Gaia DR3 Data</span>
          </span>
          <span className="flex items-center space-x-1 px-2.5 py-1 rounded-md bg-white/5 border border-white/10 text-slate-300">
            <Cpu className="w-3 h-3 text-purple-400" />
            <span>REBOUND & Symplectic N-Body Engine</span>
          </span>
          <span className="flex items-center space-x-1 px-2.5 py-1 rounded-md bg-white/5 border border-white/10 text-slate-300">
            <ShieldCheck className="w-3 h-3 text-emerald-400" />
            <span>Grounded Multi-Persona AI</span>
          </span>
        </div>

        <div className="text-right">
          <span className="text-[11px] text-slate-400">
            Active Mode: <strong className="text-slate-200 capitalize font-mono">{mode}</strong>
          </span>
        </div>
      </div>
    </footer>
  );
};
