import React, { useState } from 'react';
import { useMode } from '../context/ModeContext';
import { UserMode } from '../types/astronomy';
import {
  Settings as SettingsIcon,
  Cpu,
  Key,
  ShieldCheck,
  CheckCircle,
  RotateCcw,
  Sliders,
  Layers,
  Sparkles
} from 'lucide-react';

export const SettingsPage: React.FC = () => {
  const { mode, setMode, units, setUnits } = useMode();

  const [aiProvider, setAiProvider] = useState(() => localStorage.getItem('nebula_ai_provider') || 'auto');
  const [apiKey, setApiKey] = useState(() => localStorage.getItem('nebula_custom_api_key') || '');
  const [integrator, setIntegrator] = useState(() => localStorage.getItem('nebula_integrator') || 'ias15');
  const [saveSuccess, setSaveSuccess] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    localStorage.setItem('nebula_ai_provider', aiProvider);
    localStorage.setItem('nebula_custom_api_key', apiKey);
    localStorage.setItem('nebula_integrator', integrator);
    setSaveSuccess(true);
    setTimeout(() => setSaveSuccess(false), 3000);
  };

  const handleReset = () => {
    setMode('citizen');
    setUnits('astronomical');
    setAiProvider('auto');
    setApiKey('');
    setIntegrator('ias15');
    localStorage.clear();
    setSaveSuccess(true);
    setTimeout(() => setSaveSuccess(false), 3000);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-10">
      {/* Header */}
      <div>
        <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-sky-500/10 text-sky-300 border border-sky-400/20 text-xs font-mono mb-2">
          <SettingsIcon className="w-3.5 h-3.5" />
          <span>System Preferences & Telemetry Configuration</span>
        </div>
        <h1 className="text-3xl font-extrabold text-white">
          Application Settings
        </h1>
      </div>

      {saveSuccess && (
        <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs flex items-center space-x-2">
          <CheckCircle className="w-4 h-4 flex-shrink-0" />
          <span>Configuration saved successfully!</span>
        </div>
      )}

      <form onSubmit={handleSave} className="space-y-8">
        {/* User Experience Mode */}
        <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-white/10 space-y-5">
          <div className="flex items-center space-x-2 text-sky-400">
            <Layers className="w-5 h-5" />
            <h3 className="text-lg font-bold text-white">Default Persona Mode</h3>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {[
              { id: 'citizen' as UserMode, label: 'Citizen', desc: 'Plain English, wonder, 3D visual fidelity' },
              { id: 'student' as UserMode, label: 'Student', desc: 'Educational scaffolding, Kepler sandbox' },
              { id: 'researcher' as UserMode, label: 'Researcher', desc: 'Formal LaTeX, secular dynamics, telemetry' }
            ].map((m) => (
              <button
                key={m.id}
                type="button"
                onClick={() => setMode(m.id)}
                className={`p-4 rounded-2xl border text-left transition-all ${
                  mode === m.id
                    ? 'bg-sky-500/10 border-sky-400 text-white shadow-md'
                    : 'bg-space-900 border-white/5 text-slate-400 hover:text-white'
                }`}
              >
                <span className="font-bold text-sm block">{m.label}</span>
                <span className="text-[11px] text-slate-300 mt-1 block">{m.desc}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Physical Measurement Units */}
        <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-white/10 space-y-5">
          <div className="flex items-center space-x-2 text-amber-400">
            <Sliders className="w-5 h-5" />
            <h3 className="text-lg font-bold text-white">Physical Measurement Units</h3>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <label className="flex items-center space-x-3 p-4 rounded-2xl bg-space-900 border border-white/5 cursor-pointer">
              <input
                type="radio"
                name="units"
                checked={units === 'astronomical'}
                onChange={() => setUnits('astronomical')}
                className="w-4 h-4 accent-amber-500"
              />
              <div className="text-xs">
                <span className="text-white font-bold block">Astronomical System</span>
                <span className="text-slate-400 text-[11px]">Distances in AU, Mass in Earth masses ($M_\oplus$), Time in Earth days</span>
              </div>
            </label>

            <label className="flex items-center space-x-3 p-4 rounded-2xl bg-space-900 border border-white/5 cursor-pointer">
              <input
                type="radio"
                name="units"
                checked={units === 'si'}
                onChange={() => setUnits('si')}
                className="w-4 h-4 accent-amber-500"
              />
              <div className="text-xs">
                <span className="text-white font-bold block">Standard SI Units</span>
                <span className="text-slate-400 text-[11px]">Distances in meters/km, Mass in kilograms (kg), Time in seconds</span>
              </div>
            </label>
          </div>
        </div>

        {/* AI Provider & API Key Configuration */}
        <div className="p-6 sm:p-8 rounded-3xl glass-panel border border-white/10 space-y-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2 text-purple-400">
              <Key className="w-5 h-5" />
              <h3 className="text-lg font-bold text-white">Grounded AI Service Provider</h3>
            </div>
            <span className="px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs font-mono flex items-center space-x-1">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>Offline Fallback Always Operational</span>
            </span>
          </div>

          <p className="text-xs text-slate-300 leading-relaxed">
            NEBULA features a provider-agnostic AI layer. If no external key is configured, the deterministic
            knowledge synthesis engine automatically generates grounded, persona-adapted responses.
          </p>

          <div className="space-y-4">
            <div>
              <label className="text-xs text-slate-300 block mb-1">AI Provider</label>
              <select
                value={aiProvider}
                onChange={(e) => setAiProvider(e.target.value)}
                className="w-full bg-space-900 border border-white/10 rounded-xl px-4 py-2.5 text-xs text-white"
              >
                <option value="auto">Automatic (Gemini / OpenAI with local deterministic fallback)</option>
                <option value="gemini">Google Gemini API</option>
                <option value="openai">OpenAI GPT-4o-mini API</option>
                <option value="fallback">Local Grounded Deterministic Knowledge Engine (Offline)</option>
              </select>
            </div>

            <div>
              <label className="text-xs text-slate-300 block mb-1">API Key (Optional)</label>
              <input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="Enter GEMINI_API_KEY or OPENAI_API_KEY..."
                className="w-full bg-space-900 border border-white/10 rounded-xl px-4 py-2.5 text-xs text-white focus:outline-none focus:border-purple-500 font-mono"
              />
              <span className="text-[10px] text-slate-400 block mt-1">
                Keys are never hardcoded or transmitted elsewhere; they reside in your local environment.
              </span>
            </div>
          </div>
        </div>

        {/* Buttons */}
        <div className="flex items-center justify-between pt-4">
          <button
            type="button"
            onClick={handleReset}
            className="px-4 py-2.5 rounded-xl bg-white/5 hover:bg-white/10 text-slate-400 hover:text-white text-xs font-medium flex items-center space-x-1.5 transition-all"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Reset All to Defaults</span>
          </button>

          <button
            type="submit"
            className="px-6 py-2.5 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs transition-all shadow-md shadow-sky-600/20"
          >
            Save Configuration
          </button>
        </div>
      </form>
    </div>
  );
};
