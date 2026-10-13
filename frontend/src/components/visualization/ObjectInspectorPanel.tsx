import React from 'react';
import { Link } from 'react-router-dom';
import { AstronomicalObject, UserMode } from '../../types/astronomy';
import {
  ArrowRight,
  Crosshair,
  BarChart2,
  Bot,
  ExternalLink,
  ShieldCheck,
  GraduationCap,
  Sparkles,
  Cpu,
  Info,
  X,
} from 'lucide-react';

interface ObjectInspectorPanelProps {
  object: AstronomicalObject | null;
  mode: UserMode;
  onFocusCamera: () => void;
  onClose: () => void;
  liveState?: {
    x: number;
    y: number;
    z: number;
    trueAnomalyDeg: number;
    currentDistanceAU: number;
    instantaneousVelocityKmS: number;
  } | null;
}

export const ObjectInspectorPanel: React.FC<ObjectInspectorPanelProps> = ({
  object,
  mode,
  onFocusCamera,
  onClose,
  liveState,
}) => {
  if (!object) return null;

  const colorHex = object.color_hex || '#38bdf8';

  return (
    <div className="glass-panel-glow rounded-3xl border border-white/10 p-5 space-y-4 shadow-2xl animate-fade-in relative">
      {/* Close button */}
      <button
        onClick={onClose}
        className="absolute top-4 right-4 text-slate-400 hover:text-white p-1 rounded-lg hover:bg-white/5 transition-colors"
        title="Close Inspector"
      >
        <X className="w-4 h-4" />
      </button>

      {/* Header Profile */}
      <div className="flex items-center space-x-3 pr-8">
        <span
          className="w-4 h-4 rounded-full shadow-md flex-shrink-0 animate-pulse"
          style={{ backgroundColor: colorHex }}
        />
        <div>
          <div className="flex items-center space-x-2">
            <h3 className="text-xl font-extrabold text-white">{object.name}</h3>
            <span className="text-[10px] px-2 py-0.5 rounded-full bg-sky-500/10 text-sky-300 border border-sky-400/20 font-mono">
              {object.category}
            </span>
          </div>
          <p className="text-[11px] text-slate-400 font-mono">
            {object.parent_body_id ? `Orbiting: ${object.parent_body_id.toUpperCase()}` : 'Central Gravitational Body'}
          </p>
        </div>
      </div>

      {/* Mode-Adaptive Insight Description */}
      <div className="p-3.5 rounded-2xl bg-space-900/80 border border-white/5 space-y-1.5">
        <div className="flex items-center space-x-1.5 text-xs font-semibold">
          {mode === 'citizen' && <Sparkles className="w-3.5 h-3.5 text-purple-400" />}
          {mode === 'student' && <GraduationCap className="w-3.5 h-3.5 text-amber-400" />}
          {mode === 'researcher' && <Cpu className="w-3.5 h-3.5 text-sky-400" />}
          <span className="text-white capitalize text-[11px] font-sans">
            {mode === 'citizen'
              ? 'Plain-Language Overview'
              : mode === 'student'
              ? 'Educational Concept & Keplerian Dynamics'
              : 'Empirical Astrometric Telemetry'}
          </span>
        </div>

        <p className="text-xs text-slate-200 leading-relaxed font-sans">
          {mode === 'citizen'
            ? object.description_citizen || object.description_student
            : mode === 'student'
            ? object.description_student || object.description_citizen
            : object.description_researcher || object.description_student}
        </p>

        {/* Student Educational Tip */}
        {mode === 'student' && object.semi_major_axis_au && object.semi_major_axis_au > 0 && (
          <div className="pt-2 border-t border-white/5 text-[11px] text-amber-300/90 font-sans">
            💡 <strong>Kepler's Harmonic Rule:</strong> Orbital period ({Math.round(object.orbital_period_days || 0)} d) squared is proportional to semi-major axis cubed ($P^2 \propto a^3$).
          </div>
        )}

        {/* Researcher Live Orbit State */}
        {mode === 'researcher' && liveState && (
          <div className="pt-2 border-t border-white/5 space-y-1 font-mono text-[10px] text-sky-300">
            <div className="flex justify-between">
              <span className="text-slate-400">Instantaneous Heliocentric Distance ($r$):</span>
              <span className="font-bold text-white">{liveState.currentDistanceAU.toFixed(4)} AU</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Orbital Velocity Vector Magnitude ($v$):</span>
              <span className="font-bold text-white">{liveState.instantaneousVelocityKmS.toFixed(2)} km/s</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">True Anomaly ($\nu$):</span>
              <span className="font-bold text-white">{liveState.trueAnomalyDeg.toFixed(2)}°</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Coordinates (X, Y, Z) visual:</span>
              <span className="text-slate-300">[{liveState.x.toFixed(1)}, {liveState.y.toFixed(1)}, {liveState.z.toFixed(1)}]</span>
            </div>
          </div>
        )}
      </div>

      {/* Key Properties Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-center text-xs font-mono">
        <div className="p-2.5 rounded-xl bg-space-900 border border-white/5">
          <span className="text-[10px] text-slate-400 block font-sans">Distance ($a$)</span>
          <span className="text-white font-bold">{object.semi_major_axis_au !== null && object.semi_major_axis_au !== undefined ? `${object.semi_major_axis_au} AU` : '—'}</span>
        </div>
        <div className="p-2.5 rounded-xl bg-space-900 border border-white/5">
          <span className="text-[10px] text-slate-400 block font-sans">Orbital Period ($P$)</span>
          <span className="text-white font-bold">{object.orbital_period_days ? `${Math.round(object.orbital_period_days)} d` : '—'}</span>
        </div>
        <div className="p-2.5 rounded-xl bg-space-900 border border-white/5">
          <span className="text-[10px] text-slate-400 block font-sans">Surface Gravity ($g$)</span>
          <span className="text-white font-bold">{object.surface_gravity_m_s2 ? `${object.surface_gravity_m_s2} m/s²` : '—'}</span>
        </div>
        <div className="p-2.5 rounded-xl bg-space-900 border border-white/5">
          <span className="text-[10px] text-slate-400 block font-sans">Mean Temp ($T$)</span>
          <span className="text-white font-bold">{object.surface_temperature_k ? `${object.surface_temperature_k} K` : '—'}</span>
        </div>
      </div>

      {/* Source Provenance */}
      <div className="flex items-center justify-between text-[11px] text-slate-400 px-1 font-mono">
        <div className="flex items-center space-x-1.5">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
          <span>Source: {object.data_source || 'NASA Planetary Fact Sheet'}</span>
        </div>
        {object.source_metadata?.provenance_badge && (
          <span className="text-emerald-400">{object.source_metadata.provenance_badge}</span>
        )}
      </div>

      {/* Interactive Action Bar */}
      <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-white/10">
        {/* Focus Camera Button */}
        <button
          onClick={onFocusCamera}
          className="px-3 py-1.5 rounded-xl bg-sky-500/20 border border-sky-400/30 hover:bg-sky-500/30 text-sky-200 text-xs font-semibold flex items-center space-x-1.5 transition-all"
        >
          <Crosshair className="w-3.5 h-3.5 text-sky-400" />
          <span>Focus Camera</span>
        </button>

        {/* Open Details Link */}
        <Link
          to={`/object/${object.id}`}
          className="px-3.5 py-1.5 rounded-xl bg-sky-500 hover:bg-sky-400 text-space-950 text-xs font-bold flex items-center space-x-1.5 transition-all shadow-md shadow-sky-500/20"
        >
          <span>Open Details</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>

        {/* Compare Link */}
        <Link
          to={`/compare?target=${object.id}`}
          className="px-3 py-1.5 rounded-xl bg-white/5 hover:bg-white/10 text-slate-300 text-xs font-medium flex items-center space-x-1 transition-all"
        >
          <BarChart2 className="w-3.5 h-3.5 text-purple-400" />
          <span>Compare</span>
        </Link>

        {/* Ask AI Link */}
        <Link
          to={`/ai?target=${object.id}`}
          className="px-3 py-1.5 rounded-xl bg-white/5 hover:bg-white/10 text-slate-300 text-xs font-medium flex items-center space-x-1 transition-all"
        >
          <Bot className="w-3.5 h-3.5 text-emerald-400" />
          <span>Ask AI</span>
        </Link>
      </div>
    </div>
  );
};
